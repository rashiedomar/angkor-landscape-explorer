"""Complete document/provenance export without repeating raster/vector preparation."""
from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[1]
PROJECT=ROOT.parent
SOURCE=PROJECT/"SHARE_WITH_SCOTT/02_GIS/Angkor"
docs=ROOT/"dist/documents";docs.mkdir(exist_ok=True)
shutil.copytree(SOURCE/"sources",docs/"sources",dirs_exist_ok=True,ignore=shutil.ignore_patterns("._*"))
files=[]
for file in sorted((PROJECT/"SHARE_WITH_SCOTT").rglob("*")):
    if not file.is_file() or file.name.startswith(".") or file.name.endswith("~"):continue
    files.append({"path":file.relative_to(PROJECT/"SHARE_WITH_SCOTT").as_posix(),"bytes":file.stat().st_size})
(docs/"package_manifest.json").write_text(json.dumps({"source":"Current local SHARE_WITH_SCOTT folder; not the earlier ZIP snapshot","files":files},indent=2))
sources=[]
for file in sorted((SOURCE/"rasters").glob("*.tif")):
    if file.name.startswith("."):continue
    h=hashlib.sha256()
    with file.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):h.update(chunk)
    sources.append({"file":"02_GIS/Angkor/rasters/"+file.name,"sha256":h.hexdigest()})
(docs/"source_manifest.json").write_text(json.dumps({"display_derivatives_of":"Current SHARE_WITH_SCOTT/02_GIS/Angkor","sources":sources,"field_geometry_simplification_degrees":.000006,"source_field_features":205703},indent=2))
catalogue_path=ROOT/"dist/data/catalogue.json"
catalogue=json.loads(catalogue_path.read_text())
catalogue["sharedFiles"]=files
catalogue["sharedFolderChangedAfterZip"]=True
catalogue_path.write_text(json.dumps(catalogue,separators=(",",":")))
print(json.dumps({"field_features":catalogue["fieldCount"],"field_tiles":len(catalogue["fieldTiles"]),"shared_files":len(files),"dist_megabytes":round(sum(f.stat().st_size for f in (ROOT/"dist").rglob("*") if f.is_file())/1e6,1)}))
