"""Domain D/E: real Vila-seca friction, P2 scenarios and persisted cost paths.

The shared native producer owns input copying/rebasing, runtime, projects,
captures, closure and seals. This module owns only this activity's model,
independent numerical checks and presentation choices.
"""
import heapq
import math
from pathlib import Path
import shutil
import sqlite3


def _grid(context):
    bounds = context.parameters['bounds']
    resolution = context.parameters['resolution_m']
    width = int((bounds[2] - bounds[0]) / resolution)
    height = int((bounds[3] - bounds[1]) / resolution)
    return bounds, resolution, width, height


def _calculate(context, expression, inputs, product):
    from qgis.analysis import QgsRasterCalculator, QgsRasterCalculatorEntry
    from qgis.core import QgsProject, QgsRasterLayer, QgsRectangle
    bounds, _, width, height = _grid(context)
    layers, entries = [], []
    for name, path in inputs.items():
        layer = QgsRasterLayer(str(path), name)
        if not layer.isValid():
            raise ValueError('Invalid D/E raster input: ' + name)
        layers.append(layer)
        entry = QgsRasterCalculatorEntry()
        entry.ref, entry.raster, entry.bandNumber = name + '@1', layer, 1
        entries.append(entry)
    calculator = QgsRasterCalculator(expression, context.output(product), 'GTiff',
                                      QgsRectangle(*bounds), width, height, entries,
                                      QgsProject.instance().transformContext())
    if calculator.processCalculation() != QgsRasterCalculator.Success:
        raise ValueError(calculator.lastError())


def compute(context):
    from osgeo import gdal
    from qgis.core import QgsProject
    gdal.UseExceptions()
    context.copy_inputs()
    shutil.copyfile('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', context.output('font-regular'))
    QgsProject.instance().setEllipsoid('NONE')
    gpkg = context.output('initial-data')
    bounds, resolution, _, _ = _grid(context)
    extent = f'{bounds[0]},{bounds[2]},{bounds[1]},{bounds[3]} [EPSG:25831]'
    layer = lambda name: gpkg + '|layername=' + name

    context.processing('native:buffer', {
        'INPUT': layer('autopista_eixos'), 'DISTANCE': context.parameters['axis_buffer_m'],
        'SEGMENTS': 8, 'DISSOLVE': True, 'OUTPUT': context.output('axis-buffer'),
    })
    context.processing('native:extractbyattribute', {
        'INPUT': layer('cobertes'), 'FIELD': 'classe', 'OPERATOR': 0, 'VALUE': 351,
        'OUTPUT': context.output('road-cover'),
    })
    context.processing('native:intersection', {
        'INPUT': context.output('road-cover'), 'OVERLAY': context.output('axis-buffer'),
        'OUTPUT': context.output('barrier-vector'),
    })
    for product, source, field, burn in [
        ('classes', layer('cobertes'), 'classe', 0),
        ('pass-grid', layer('passos'), 'pas_id', 0),
        ('barrier-grid', context.output('barrier-vector'), None, 1),
    ]:
        context.processing('gdal:rasterize', {
            'INPUT': source, 'FIELD': field, 'BURN': burn, 'UNITS': 1,
            'WIDTH': resolution, 'HEIGHT': resolution, 'EXTENT': extent,
            'INIT': 0, 'NODATA': -9999, 'DATA_TYPE': 5, 'OUTPUT': context.output(product),
        })
    connection = sqlite3.connect('file:' + gpkg + '?mode=ro', uri=True)
    try:
        costs = connection.execute('SELECT classe, cost_model FROM llegenda_costos ORDER BY classe').fetchall()
    finally:
        connection.close()
    table = [0, 0, 99]
    for code, weight in costs:
        table.extend([code, code, weight])
    context.processing('native:reclassifybytable', {
        'INPUT_RASTER': context.output('classes'), 'RASTER_BAND': 1, 'TABLE': table,
        'NO_DATA': -9999, 'RANGE_BOUNDARIES': 2, 'NODATA_FOR_MISSING': True,
        'DATA_TYPE': 5, 'OUTPUT': context.output('base'),
    })
    expressions = {
        'open': 'if("pas@1" > 0, 1, if("barrera@1" > 0, 99, if("base@1" = 0, 99, "base@1")))',
        'closed': 'if("pas@1" = 1, 1, if(("pas@1" = 2) OR ("barrera@1" > 0), 99, if("base@1" = 0, 99, "base@1")))',
    }
    for state, expression in expressions.items():
        _calculate(context, expression, {
            'pas': context.output('pass-grid'), 'barrera': context.output('barrier-grid'),
            'base': context.output('base'),
        }, 'friction-numeric-' + state)
        image = gdal.Translate(context.output('friction-' + state),
                               context.output('friction-numeric-' + state), noData=99)
        if image is None:
            raise ValueError('Unable to persist final friction: ' + state)
        image = None
        _calculate(context, '"friccio@1" * 5',
                   {'friccio': context.output('friction-' + state)}, 'cell-cost-' + state)
        context.processing('grass:r.cost', {
            'input': context.output('cell-cost-' + state), 'start_points': layer('origen'),
            '-k': False, '-n': True, 'output': context.output('cost-' + state),
            'outdir': context.output('directions-' + state),
            'GRASS_REGION_PARAMETER': extent, 'GRASS_REGION_CELLSIZE_PARAMETER': resolution,
        })
        route = context.processing('grass:r.path', {
            'input': context.output('directions-' + state), 'format': 1,
            'start_points': layer('desti'), 'vector_path': 'TEMPORARY_OUTPUT',
            'raster_path': 'TEMPORARY_OUTPUT', 'GRASS_REGION_PARAMETER': extent,
            'GRASS_REGION_CELLSIZE_PARAMETER': resolution,
        })
        context.processing('native:savefeatures', {
            'INPUT': route['vector_path'], 'OUTPUT': context.output('route-' + state),
        })


def _read(context, product):
    from osgeo import gdal
    import numpy as np
    bounds, resolution, width, height = _grid(context)
    image = gdal.Open(context.output(product), gdal.GA_ReadOnly)
    if image is None or (image.RasterXSize, image.RasterYSize) != (width, height):
        raise ValueError('Unexpected persisted D/E grid: ' + product)
    if image.GetGeoTransform() != (bounds[0], resolution, 0., bounds[3], 0., -resolution):
        raise ValueError('D/E raster alignment changed: ' + product)
    array = image.ReadAsArray().astype(float)
    nodata = image.GetRasterBand(1).GetNoDataValue()
    array[~np.isfinite(array) | (array == nodata)] = np.nan
    image = None
    return array


def _independent_cost(cell_cost, start, end):
    """Eight-neighbour Dijkstra; cell costs already include the 5 m factor."""
    import numpy as np
    distances = np.full(cell_cost.shape, np.inf)
    distances[start] = 0.
    queue = [(0., *start)]
    moves = [(dy, dx, math.hypot(dy, dx)) for dy in (-1, 0, 1)
             for dx in (-1, 0, 1) if dy or dx]
    while queue:
        cost, y, x = heapq.heappop(queue)
        if cost != distances[y, x]:
            continue
        if (y, x) == end:
            return cost
        for dy, dx, length in moves:
            ny, nx = y + dy, x + dx
            if not (0 <= ny < cell_cost.shape[0] and 0 <= nx < cell_cost.shape[1]):
                continue
            if not np.isfinite(cell_cost[ny, nx]):
                continue
            candidate = cost + length * (cell_cost[y, x] + cell_cost[ny, nx]) / 2
            if candidate < distances[ny, nx]:
                distances[ny, nx] = candidate
                heapq.heappush(queue, (candidate, ny, nx))
    raise ValueError('The persisted D/E grid does not connect O and D')


def verify(context):
    import numpy as np
    from qgis.core import QgsVectorLayer
    gpkg = context.output('initial-data')
    bounds, resolution, width, height = _grid(context)
    points = []
    for name in ('origen', 'desti'):
        layer = QgsVectorLayer(gpkg + '|layername=' + name, name, 'ogr')
        if not layer.isValid() or layer.featureCount() != 1:
            raise ValueError('Invalid persisted D/E endpoint: ' + name)
        point = next(layer.getFeatures()).geometry().asPoint()
        points.append((point.x(), point.y()))
    start, end = [(int((bounds[3] - y) / resolution), int((x - bounds[0]) / resolution)) for x, y in points]
    checks = []

    def check(identity, actual, expected, tolerance=0, units='count'):
        checks.append(dict(id=identity, actual=float(actual), expected=float(expected),
                           tolerance=tolerance, units=units))

    check('grid-columns', width, 600)
    check('grid-rows', height, 640)
    for actual, name in zip(points, ('origin', 'destination')):
        check(name + '-coordinates', math.dist(actual, context.parameters[name]), 0, .001, 'm')
    passes = _read(context, 'pass-grid')
    barrier = _read(context, 'barrier-grid')
    base = _read(context, 'base')
    p2 = tuple(context.parameters['p2_cell'])
    alternative = tuple(context.parameters['alternative_cell'])
    for state in ('open', 'closed'):
        numeric = _read(context, 'friction-numeric-' + state)
        friction = _read(context, 'friction-' + state)
        cell_cost = _read(context, 'cell-cost-' + state)
        accumulated = _read(context, 'cost-' + state)
        allowed = passes > 0 if state == 'open' else passes == 1
        excluded = (barrier > 0) | ((passes == 2) if state == 'closed' else False)
        independent = np.where(allowed, 1, np.where(excluded, 99, np.where(base == 0, 99, base)))
        check('conditional-' + state, np.count_nonzero(numeric != independent), 0)
        check('cell-scale-' + state, np.nanmax(np.abs(cell_cost - friction * resolution)), 0, 1e-6, 'weighted-m')
        check('nodata-preserved-' + state, np.count_nonzero(np.isnan(cell_cost) != np.isnan(friction)), 0)
        check('alternative-' + state, cell_cost[alternative], 5, units='weighted-m')
        if state == 'open':
            check('p2-open', cell_cost[p2], 5, units='weighted-m')
        else:
            check('p2-closed-nodata', int(np.isnan(cell_cost[p2])), 1)
        expected = context.parameters['expected'][state]
        worldfile_expected = (resolution, 0, 0, -resolution,
                              bounds[0] + resolution / 2, bounds[3] - resolution / 2)
        for prefix in ('cost', 'directions'):
            worldfile = tuple(float(value) for value in Path(context.output(prefix + '-' + state + '-worldfile')).read_text().split())
            if len(worldfile) != 6:
                raise ValueError('Invalid persisted D/E worldfile: ' + prefix + '-' + state)
            check(prefix + '-worldfile-' + state, max(abs(a - b) for a, b in zip(worldfile, worldfile_expected)), 0, 1e-9, 'm')
        check('cost-d-' + state, accumulated[end], expected['cost_weighted_m'], .02, 'weighted-m')
        check('dijkstra-' + state, accumulated[end], _independent_cost(cell_cost, start, end), .02, 'weighted-m')
        layer_name = 'ruta_cost_obert' if state == 'open' else 'ruta_cost_tancat'
        route = QgsVectorLayer(context.output('route-' + state) + '|layername=' + layer_name, layer_name, 'ogr')
        if not route.isValid() or route.featureCount() < 1 or route.crs().authid() != 'EPSG:25831':
            raise ValueError('Invalid persisted D/E route: ' + state)
        check('route-length-' + state, sum(f.geometry().length() for f in route.getFeatures()),
              expected['path_length_m'], .02, 'm')
    return checks


def compose(project, project_id, parameters, products):
    """Only teaching presentation; shared code saves/checks/captures the project."""
    from qgis.core import (QgsRectangle, QgsReferencedRectangle, QgsTextFormat, QgsLineSymbol,
                          QgsRasterShader, QgsColorRampShader, QgsSingleBandPseudoColorRenderer)
    from qgis.PyQt.QtGui import QFont, QColor
    project.setEllipsoid('NONE')
    project.setTitle('Accessibilitat de Vila-seca · ' + ('cost P2 D/E' if project_id == 'resolved-project' else 'inici D/E'))
    text = QgsTextFormat()
    text.setFont(QFont('DejaVu Sans'))
    project.styleSettings().setDefaultTextFormat(text)
    project.viewSettings().setDefaultViewExtent(QgsReferencedRectangle(QgsRectangle(*parameters['bounds']), project.crs()))
    if project_id != 'resolved-project':
        return
    for name, colour in [('Camí de cost · obert', '#00866f'), ('Camí de cost · tancat', '#ba3545')]:
        layer = project.mapLayersByName(name)[0]
        layer.renderer().setSymbol(QgsLineSymbol.createSimple({'line_color': colour, 'line_width': '1.2'}))
    for name in ('Cost acumulat · obert', 'Cost acumulat · tancat'):
        layer = project.mapLayersByName(name)[0]
        ramp = QgsColorRampShader()
        ramp.setColorRampType(QgsColorRampShader.Interpolated)
        ramp.setColorRampItemList([QgsColorRampShader.ColorRampItem(value, QColor(colour), str(value))
                                   for value, colour in [(0, '#fff7ec'), (1500, '#fec44f'), (4500, '#d95f0e'), (10000, '#7f0000')]])
        ramp.setMinimumValue(0)
        ramp.setMaximumValue(10000)
        shader = QgsRasterShader()
        shader.setRasterShaderFunction(ramp)
        layer.setRenderer(QgsSingleBandPseudoColorRenderer(layer.dataProvider(), 1, shader))
    for layer in project.mapLayers().values():
        node = project.layerTreeRoot().findLayer(layer.id())
        node.setItemVisibilityChecked(layer.name() in {
            'Cost acumulat · obert', 'Camí de cost · obert', 'Camí de cost · tancat',
            'Origen O', 'Destí D', 'P2 principal i passos alternatius',
        })
