"""Drawing helpers for this manual's aggregate census-section figures."""
import json
from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.path import Path as MplPath
from matplotlib.patches import PathPatch
import numpy as np


def load(root):
    folder = Path(root) / 'context/inputs'
    features = json.loads((folder / 'seccions-tarragones.geojson').read_text())['features']
    result = json.loads((folder / 'seccions-resultats.json').read_text())
    assert len(features) == result['section_count'] == 151
    plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 14,
                         'svg.fonttype': 'none'})
    return features, result


def polygons(geometry):
    return geometry['coordinates'] if geometry['type'] == 'MultiPolygon' else [geometry['coordinates']]


def draw(ax, features, colour, title, extent=None):
    vertices = []
    for feature in features:
        for polygon in polygons(feature['geometry']):
            rings = [np.asarray(ring)[:, :2] / 1000 for ring in polygon]
            vertices.extend(rings)
            paths = [MplPath(ring, [MplPath.MOVETO] + [MplPath.LINETO] * (len(ring)-2)
                             + [MplPath.CLOSEPOLY]) for ring in rings]
            ax.add_patch(PathPatch(MplPath.make_compound_path(*paths),
                                   facecolor=colour(feature['properties']),
                                   edgecolor='#59636c', lw=.35))
    xy = np.concatenate(vertices)
    if extent is None:
        lo, hi = xy.min(axis=0), xy.max(axis=0)
        extent = [lo[0]-1, hi[0]+1, lo[1]-1, hi[1]+1]
    ax.set(xlim=extent[:2], ylim=extent[2:], aspect='equal', title=title,
           xlabel='Est UTM (km)', ylabel='Nord UTM (km)')
    ax.ticklabel_format(useOffset=False, style='plain')
    ax.tick_params(labelsize=14)
    ax.set_facecolor('#f8fafc')
    ax.annotate('N', xy=(.94, .95), xytext=(.94, .78), xycoords='axes fraction',
                ha='center', va='center', arrowprops={'arrowstyle':'->', 'lw':1.4})
    length = 5 if extent[1]-extent[0] > 15 else 1
    x, y = extent[0]+.08*(extent[1]-extent[0]), extent[2]+.87*(extent[3]-extent[2])
    ax.plot([x, x+length], [y, y], color='#17293c', lw=2.5)
    ax.text(x+length/2, y+.025*(extent[3]-extent[2]), f'{length} km', ha='center', fontsize=14)


def save(fig, root, name):
    out = Path(root) / 'assets/img/generated' / (name + '.svg')
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, facecolor='white', metadata={'Date': None})
    plt.close(fig)
