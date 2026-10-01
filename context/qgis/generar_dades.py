"""Generate private synthetic inputs for the two QGIS teaching captures."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[2]
out = root / "tmp/dades-docents/qgis"
out.mkdir(parents=True, exist_ok=True)

def save(name, features):
    document = {
        "type": "FeatureCollection",
        "name": name,
        "crs": {"type": "name", "properties": {"name": "EPSG:25831"}},
        "features": features,
    }
    path = out / f"{name}.geojson"
    text = json.dumps(document, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text() != text:
        raise FileExistsError(f"Different existing input: {path}")
    if not path.exists():
        path.write_text(text)
    print(path.relative_to(root))

points = [(0, 0, 10), (4, 0, 10), (0, 4, 20), (4, 4, 60)]
save("centres", [
    {"type": "Feature", "properties": {"id": f"P{i}", "POT_KW": p},
     "geometry": {"type": "Point", "coordinates": [350000 + 1000*x, 4550000 + 1000*y]}}
    for i, (x, y, p) in enumerate(points, 1)
])
nodes = {"O": (1, 2), "A": (1, 5), "B": (7, 5), "D": (7, 2),
         "E": (1, 6), "F": (7, 6), "G": (3, 2), "H": (8, 2)}
edges = [("O", "A"), ("A", "B"), ("B", "D"), ("A", "E"),
         ("E", "F"), ("F", "B"), ("O", "G"), ("D", "H")]
save("xarxa", [
    {"type": "Feature", "properties": {"id": f"{u}-{v}", "vel_kmh": 30},
     "geometry": {"type": "LineString", "coordinates": [
         [350000+100*nodes[k][0], 4550000+100*nodes[k][1]] for k in (u, v)]}}
    for u, v in edges
])
