# Angkor landscape explorer

A buildless, source-linked map of existing Angkor data. This is a presentation and exploration layer, not new scientific analysis. The website does not add new observations, verified crop classes, ancient-feature dates or a drainage model.

## Start locally

Run `/usr/bin/python3 code/serve.py` from this folder, then open **http://127.0.0.1:8765**. The server binds only to loopback and exposes `dist/` plus explicitly restricted downloads from the neighbouring `SHARE_WITH_SCOTT` folder. It does not serve QGIS profiles, caches, authentication databases or the whole external drive.

The map opens with the dry RGB background and within-2025 seasonal-water contrast. Switch dry/wet/terrain, inspect a map point, change analytical layers, or enable field outlines at zoom 14+. A 12,000-visible-prediction limit asks the viewer to zoom closer rather than silently selecting examples. All 205,703 source predictions are retained across browser chunks; rendered geometry is simplified slightly. Metadata, methods and limitations are available on demand.

The closable research-notes drawer separates the professor's directions, paper takeaways and current progress. It explicitly retains unfinished reading, other-region GIS packages, wider landscape extents, DEM/drainage work and validation gaps.

## Data preparation

Use the existing Python 3.9 geospatial environment on KIOXIA:

```
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH='/Volumes/KIOXIA/Prof. Scott/Landesque_Pilot/.python_packages' /usr/bin/python3 code/prepare_data.py
```

`code/finish_assets.py` refreshes document/source manifests without repeating the raster/vector conversion. Nothing in either script edits the original GIS rasters, GeoPackage or scientific metrics. Raster web layers are reprojected to Web Mercator, and click inspection uses nearest display samples except the interpolated terrain display. Statistics refer to the original UTM grid, not web geometry. `dist/documents/source_manifest.json` records the source-raster hashes.

The current upload folder was edited after the earlier ZIP snapshot: it now includes `04_Sources_provided_by_professor_Scott` and no longer contains the original root README/manifest. This explorer inventories the current folder without overwriting those edits or presenting the older ZIP as identical.

## Published dashboard

Dashboard: https://rashiedomar.github.io/angkor-landscape-explorer/

Source: https://github.com/rashiedomar/angkor-landscape-explorer

GitHub Pages serves the static `dist/` directory from the `gh-pages` branch. Original GIS files are supplied separately. The shared Drive URL is pending; the public dashboard labels unavailable download links accordingly. Set `driveUrl` in `dist/data/catalogue.json` when that URL is available.

The site includes selected research directions and reading notes, with scientific limitations visible in the interface. Original papers, full GIS downloads, local review captures and private runtime files are excluded from this repository. University branding does not indicate endorsement.

Vendored Leaflet and pako licence files are in `dist/vendor/`.

Logo source: https://adelaide.edu.au/content/dam/adelaideuniversity/images/global/logos/au-logo-dark-blue-horizontal.svg

The browser map runs locally without external tile services, map analytics, CDN requests or sign-in. Links to original provider websites open only when deliberately selected. Google Drive sharing settings remain under the owner's control.
