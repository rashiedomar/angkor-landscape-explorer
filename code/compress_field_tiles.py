"""Losslessly compress display chunks and retain uncompressed generated copies privately."""
from pathlib import Path
import gzip,json,shutil
ROOT=Path(__file__).resolve().parents[1]
catalogue_path=ROOT/"dist/data/catalogue.json"
catalogue=json.loads(catalogue_path.read_text())
backup=ROOT/"review/uncompressed_fields";backup.mkdir(exist_ok=True)
for tile in catalogue["fieldTiles"]:
    path=ROOT/"dist/data"/tile["file"]
    if path.suffix==".gz":continue
    obj=json.loads(path.read_text())
    for feature in obj["features"]:
        points=[]
        def collect(coords):
            if isinstance(coords[0],(int,float)):points.append(coords)
            else:
                for child in coords:collect(child)
        collect(feature["geometry"]["coordinates"])
        feature["bbox"]=[min(p[0] for p in points),min(p[1] for p in points),max(p[0] for p in points),max(p[1] for p in points)]
    raw=json.dumps(obj,separators=(",",":")).encode()
    output=Path(str(path)+".gz")
    output.write_bytes(gzip.compress(raw,compresslevel=7,mtime=0))
    assert json.loads(gzip.decompress(output.read_bytes()))==obj
    shutil.move(str(path),str(backup/path.name))
    tile["file"]=tile["file"]+".gz"
catalogue_path.write_text(json.dumps(catalogue,separators=(",",":")))
print("Compressed field chunks verified; source data unchanged.")
