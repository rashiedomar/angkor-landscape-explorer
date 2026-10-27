# Terrain audit

Measured from the existing cached DSMs, not new field measurements.

| Region | P05 (m) | Median (m) | P95 (m) | P95-P05 (m) | Full range (m) |
|---|---:|---:|---:|---:|---:|
| Angkor | 5.3 | 17.0 | 55.6 | 50.3 | 0.0 to 367.5 |
| Srei Santhor / Tuol Basan | 3.6 | 8.3 | 13.2 | 9.6 | -17.0 to 94.0 |
| Sukhothai | 45.1 | 60.0 | 380.3 | 335.2 | 32.1 to 1233.0 |
| Prambanan | 52.1 | 191.4 | 748.2 | 696.1 | 7.0 to 2258.0 |

## What this means

The Java box has the greatest broad elevation variation. The Sukhothai box also includes substantial high ground: do not treat all of Thailand as flat. Srei Santhor's negative tail (minimum about -17 m) needs examination against water coverage, editing masks and another terrain source. Negative values alone do not prove an error; neither should they be accepted as surveyed ground elevations.

All four local rasters have finite values throughout their analytical boxes. This is a file-coverage check, not an accuracy assessment. They carry horizontal UTM CRSs only. Product documentation specifies EGM2008 heights in metres; no vertical transformation has been performed. The cached source-tile files are already warped, so they are not pristine native DEM tiles.

## Gate before drainage modelling or fusion

1. Retrieve native DEM windows for a landscape-context area extending beyond the old box; retain source masks and metadata. A catchment cannot be delineated reliably when its headwaters lie outside the DEM extent.
2. Check zero/nodata treatment: the earlier preparation used `a != 0` and requested zero destination fill. Preserve legitimate sea-level heights on reprocessing. Do not silently replace the original results.
3. Compare at native-compatible scale with a second documented elevation source. Check datum, units, dates, forest/urban bias, tile seams and water flattening. Do not just average DEMs or treat related products as independent.
4. Compare broad profiles and plausible outlets. Only then test routing/conditioning, with unconditioned and conditioned surfaces retained separately. Contemporary roads, embankments and canals can alter flow.
5. Quantify sensitivity to terrain source and conditioning. Do not date a feature or infer canal connectivity from a coarse DSM alone.

Source product specifications and surface-model definition: [Copernicus Data Space](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM). Published product-level accuracy is not a site-specific error measurement.
