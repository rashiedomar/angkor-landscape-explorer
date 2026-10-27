"""Validate local assets against the current upload folder, not a fictional full study."""
from pathlib import Path
import gzip,json,hashlib,urllib.request
ROOT=Path(__file__).resolve().parents[1]
DIST=ROOT/"dist"
SHARE=ROOT.parent/"SHARE_WITH_SCOTT"
catalogue=json.loads((DIST/"data/catalogue.json").read_text())
assert catalogue["driveUrl"] is None
assert catalogue["fieldCount"]==205703
assert sum(tile["count"] for tile in catalogue["fieldTiles"])==205703
total=0
for tile in catalogue["fieldTiles"]:
    data=json.loads(gzip.decompress((DIST/"data"/tile["file"]).read_bytes()))
    assert len(data["features"])==tile["count"]
    assert all("bbox" in f for f in data["features"])
    total+=len(data["features"])
pixels=catalogue["width"]*catalogue["height"]
for name,size in {"water":1,"dry-count":1,"wet-count":1,"landcover":1,"occurrence":1,"terrain":2,"vegetation":2}.items():
    assert len(gzip.decompress((DIST/"data"/(name+".bin.gz")).read_bytes()))==pixels*size
manifest=json.loads((DIST/"documents/source_manifest.json").read_text())
for source in manifest["sources"]:
    h=hashlib.sha256()
    with (SHARE/source["file"]).open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):h.update(chunk)
    assert h.hexdigest()==source["sha256"]
assert all((SHARE/file["path"]).is_file() for file in catalogue["sharedFiles"])
http_paths=["/","/style.css","/app.js","/vendor/leaflet.js","/vendor/pako_inflate.min.js","/assets/adelaide-university.svg","/data/catalogue.json","/documents/Reading_and_terrain_notes.pdf","/documents/source_manifest.json","/documents/package_manifest.json","/downloads/"]
for path in http_paths:
    with urllib.request.urlopen("http://127.0.0.1:8765"+path) as response:assert response.status==200
assert "Independent preview · not university-endorsed" not in (DIST/"index.html").read_text()
report={"field_predictions_retained":total,"field_chunks":len(catalogue["fieldTiles"]),"original_raster_checksums_matched":len(manifest["sources"]),"current_shared_files":len(catalogue["sharedFiles"]),"inspection_grids_checked":7,"http_asset_checks":len(http_paths),"all_checks_passed":True,"scope":"Asset integrity/provenance and local serving; not new thematic or archaeological validation.","browser_checks_observed":["dry/wet switch","closable notes: brief, reading notes and progress","water click inspection with observation counts","source and method dialog","vegetation, land-cover and support layer changes","high-zoom field rendering (1,642 visible predictions)","requested header text removed"],"publication":"Not published; real Drive URL and release review are pending"}
(ROOT/"review/validation.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
