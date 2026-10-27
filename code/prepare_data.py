"""Create browser derivatives of the curated Angkor package; source data unchanged."""
from pathlib import Path
import gzip
import hashlib
import json
import math
import shutil

import geopandas as gpd
import numpy as np
from PIL import Image
import rasterio
from rasterio.warp import reproject, transform_bounds, Resampling
from rasterio.transform import from_bounds

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE = PROJECT / "SHARE_WITH_SCOTT/02_GIS/Angkor"
DATA = ROOT / "dist/data"
DATA.mkdir(parents=True, exist_ok=True)
with rasterio.open(SOURCE / "rasters/water_change.tif") as src:
    native_bounds = list(src.bounds)
    merc = transform_bounds(src.crs, "EPSG:3857", *src.bounds, densify_pts=41)
    latlon = transform_bounds("EPSG:3857", "EPSG:4326", *merc)
    width = 2236
    height = round(width * (merc[3]-merc[1])/(merc[2]-merc[0]))
    target_transform = from_bounds(*merc, width, height)

def warp(name, band=1, nearest=True):
    target = np.full((height,width), np.nan, dtype=np.float32)
    with rasterio.open(SOURCE / "rasters" / name) as src:
        # Counts and JRC have meaningful zeros despite legacy nodata flags.
        source = src.read(band).astype(np.float32)
        nodata = np.nan if src.nodata is not None and np.isnan(src.nodata) else src.nodata
        if "observation_count" in name or name.startswith("jrc_"):
            nodata = None
        reproject(source, target, src_transform=src.transform, src_crs=src.crs,
                  src_nodata=nodata, dst_transform=target_transform,
                  dst_crs="EPSG:3857", dst_nodata=np.nan,
                  resampling=Resampling.nearest if nearest else Resampling.bilinear)
    return target

def save_rgba(name, rgba):
    Image.fromarray(np.nan_to_num(rgba).astype(np.uint8)).save(DATA / (name+".png"), optimize=True)

def categorical(name, values, palette, unknown=(178,182,178,125)):
    rgba = np.zeros((height,width,4), dtype=np.uint8)
    rgba[:] = unknown
    for value, color in palette.items():
        rgba[values==value] = color
    save_rgba(name, rgba)

def binary(name, values, dtype):
    raw = values.astype(dtype).tobytes()
    (DATA / (name+".bin.gz")).write_bytes(gzip.compress(raw, compresslevel=7, mtime=0))

for season in ["dry", "wet"]:
    cube = np.stack([warp(season+"_composite.tif",band,False) for band in [3,2,1]],axis=-1)
    valid = np.isfinite(cube).all(axis=2)
    rgb = np.power(np.clip(np.nan_to_num(cube)/0.30,0,1),1/1.05)*255
    save_rgba(season, np.dstack([rgb, valid.astype(np.uint8)*255]))

water = np.nan_to_num(warp("water_change.tif")).astype(np.uint8)
categorical("water",water,{0:(142,149,142,125),1:(0,0,0,0),2:(20,93,132,235),3:(62,171,194,225),4:(193,145,73,235)})
binary("water",water,"u1")
dc = np.nan_to_num(warp("dry_observation_count.tif")).astype(np.uint8)
wc = np.nan_to_num(warp("wet_observation_count.tif")).astype(np.uint8)
binary("dry-count",dc,"u1");binary("wet-count",wc,"u1")
support = np.minimum(np.minimum(dc,wc),2)
categorical("support",support,{0:(117,125,120,200),1:(222,187,116,165),2:(57,118,103,145)})

dem = warp("dem.tif",nearest=False)
stops = np.array([0,5,15,30,60,100,200,370],dtype=float)
colors = np.array([[222,230,215],[213,223,204],[197,212,185],[177,196,163],[155,175,139],[178,169,134],[166,148,122],[137,124,112]])
rgb = np.stack([np.interp(dem,stops,colors[:,i]) for i in range(3)],axis=-1)
save_rgba("terrain",np.dstack([rgb,np.isfinite(dem)*255]))
binary("terrain",np.where(np.isfinite(dem),np.round(dem*10),-32768),"<i2")

ndvi = warp("ndvi_wet_minus_dry_min2obs_2025.tif")
stops = [-1,-.4,0,.4,1]
colors = np.array([[139,93,63],[199,165,129],[244,241,230],[124,168,137],[44,105,79]])
rgb = np.stack([np.interp(np.nan_to_num(ndvi),stops,colors[:,i]) for i in range(3)],axis=-1)
save_rgba("vegetation",np.dstack([rgb,np.isfinite(ndvi)*205]))
binary("vegetation",np.where(np.isfinite(ndvi),np.round(ndvi*1000),-32768),"<i2")

cover = np.nan_to_num(warp("worldcover_2021.tif")).astype(np.uint8)
cover_colors={10:(44,93,65,200),20:(169,174,98,190),30:(199,208,126,190),40:(211,182,109,195),50:(164,99,89,210),60:(199,193,176,190),70:(244,244,241,195),80:(35,110,161,210),90:(81,158,155,195),95:(60,131,108,195),100:(183,175,143,190)}
categorical("landcover",cover,cover_colors,unknown=(0,0,0,0))
binary("landcover",cover,"u1")
jrc = warp("jrc_occurrence_1984_2024.tif")
jvalid = np.isfinite(jrc)&(jrc>=0)&(jrc<=100)
rgb=np.stack([np.interp(np.nan_to_num(jrc),[0,100],[235,25]),np.interp(np.nan_to_num(jrc),[0,100],[242,103]),np.interp(np.nan_to_num(jrc),[0,100],[244,151])],axis=-1)
save_rgba("occurrence",np.dstack([rgb,np.where(jvalid&(jrc>0),200,0)]))
binary("occurrence",np.where(jvalid,jrc,255),"u1")

print("Raster assets prepared",flush=True)
# Partition all predictions, rather than silently selecting attractive examples.
fields = gpd.read_file(SOURCE / "angkor.gpkg",layer="ftw_modelled_fields_2025").to_crs(4326)
centres = fields.geometry.representative_point()
west,south,east,north=latlon
cols=rows=10
ix=np.clip(((centres.x-west)/(east-west)*cols).astype(int),0,cols-1)
iy=np.clip(((centres.y-south)/(north-south)*rows).astype(int),0,rows-1)
index=[]
for x in range(cols):
    for y in range(rows):
        subset=fields.loc[(ix==x)&(iy==y)].copy()
        if subset.empty:continue
        subset["geometry"]=subset.geometry.simplify(.000006,preserve_topology=True)
        features=[]
        for row in subset.itertuples():
            geometry=json.loads(json.dumps(row.geometry.__geo_interface__))
            def rounded(value):
                return [rounded(v) for v in value] if isinstance(value,(list,tuple)) else round(value,6)
            geometry["coordinates"]=rounded(geometry["coordinates"])
            features.append({"type":"Feature","geometry":geometry,"bbox":[round(v,6) for v in row.geometry.bounds],"properties":{"id":str(row.id),"area_ha":round(row.clipped_area_m2/10000,3),"score":round(row.confidence,1) if np.isfinite(row.confidence) else None}})
        filename=f"fields/{x}-{y}.json.gz"
        (DATA/filename).write_bytes(gzip.compress(json.dumps({"type":"FeatureCollection","features":features},separators=(",",":")).encode(),compresslevel=7,mtime=0))
        bounds=subset.total_bounds.tolist()
        index.append({"file":filename,"bounds":bounds,"count":len(features)})

metadata={"width":width,"height":height,"mercatorBounds":list(merc),"bounds":[[south,west],[north,east]],"nativeBounds":native_bounds,"fieldCount":len(fields),"fieldTiles":index,
    "originalAreaKm2":1999.8784,"waterKm2":{"dry":76.2248,"wet":337.5672,"both":72.868,"wetOnly":264.6992,"dryOnly":3.3568},
    "commonWaterSupportPct":84.09,"vegetationSupportPct":54.0655,
    "displayNote":"Browser images and click values are reprojected display derivatives. Area totals use the original projected analysis grid, not web-map geometry. Field geometry is slightly simplified for display; full geometry is in the GeoPackage.",
    "driveUrl":None,"logoPreviewOnly":True}
(DATA/"catalogue.json").write_text(json.dumps(metadata,separators=(",",":")))
docs=ROOT/"dist/documents";docs.mkdir(exist_ok=True)
for name in ["Reading_and_terrain_notes.pdf","Terrain_audit.md","Working_reading_notes.md"]:
    shutil.copy2(PROJECT/"SHARE_WITH_SCOTT/03_Reading_and_terrain_notes"/name,docs/name)
package_manifest=[]
for file in sorted((PROJECT/"SHARE_WITH_SCOTT").rglob("*")):
    if not file.is_file() or file.name.startswith(".") or file.name.endswith("~"):continue
    package_manifest.append({"path":file.relative_to(PROJECT/"SHARE_WITH_SCOTT").as_posix(),"bytes":file.stat().st_size})
(docs/"package_manifest.json").write_text(json.dumps({"source":"Current local SHARE_WITH_SCOTT folder; not the earlier ZIP snapshot","files":package_manifest},indent=2))
shutil.copytree(SOURCE/"sources",docs/"sources",dirs_exist_ok=True,ignore=shutil.ignore_patterns("._*"))
provenance=[]
for filename in ["water_change.tif","dry_composite.tif","wet_composite.tif","dem.tif","worldcover_2021.tif","jrc_occurrence_1984_2024.tif","ndvi_wet_minus_dry_min2obs_2025.tif"]:
    file=SOURCE/"rasters"/filename
    h=hashlib.sha256()
    with file.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):h.update(chunk)
    provenance.append({"file":"02_GIS/Angkor/rasters/"+filename,"sha256":h.hexdigest()})
(docs/"source_manifest.json").write_text(json.dumps({"display_derivatives_of":"SHARE_WITH_SCOTT","sources":provenance,"field_geometry_simplification_degrees":.000006,"source_field_features":len(fields)},indent=2))
print(json.dumps({"width":width,"height":height,"field_features":len(fields),"field_tiles":len(index),"web_data_megabytes":round(sum(f.stat().st_size for f in DATA.rglob("*") if f.is_file())/1e6,1)}))
