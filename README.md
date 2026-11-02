# Madagascar: Travel Time to the Nearest Health Centre

Live map: https://dzvihxrhaf8k6.cloudfront.net/

## Dataset, licence and credit
- Source: HDX, "Madagascar Motorised Travel Time (in seconds) to nearest health centre", Data for Children Collaborative.
- Licence: CC BY 4.0 (verified on the HDX page).
- Credit: Data for Children Collaborative (2024), HDX. Watmough et al. (2022), *Scientific Data*, doi:10.1038/s41597-022-01274-w.
- Raw file: GeoTIFF, EPSG:4326, ~100 m pixels, float64.

## Health facility layer
- Source: OpenStreetMap via the Geofabrik Madagascar extract (data up to 2026-10-30), licence ODbL 1.0. Credit: © OpenStreetMap contributors.
- Extracted with pyosmium: `amenity` in hospital, clinic, doctors, health_post, or `healthcare` tags for the same types. Pharmacies, dentists and labs were left out. Result: 1,469 points (320 hospitals, 116 clinics, 265 health posts, 768 doctors), saved as `madagascar_health_facilities_filtered.geojson` and served from `/data/`.
- This is a different source from the travel-time dataset. OSM mapping is uneven (dense on the east coast and around the capital), so an empty area may mean unmapped, not no facility.

## AWS services and why
- **Amazon S3**: private bucket (all public access blocked, SSE-S3 encryption) holding `/site/` and `/data/`.
- **Amazon CloudFront** with Origin Access Control: serves the site and data over HTTPS; only the distribution can read the bucket.
- **Amazon Location Service**: base map tiles via a referrer-restricted API key .

## Pipeline
1. Raster downsampled 4x and polygonised into four bands (under 1 h, 1-2 h, 2-4 h, over 4 h) with rasterio and shapely, simplified at tolerance 0.002.
2. Attribution added to the GeoJSON; all features checked against lon 43-51, lat -26 to -11.5 (none outside).
3. For speed, bands were further simplified (Douglas-Peucker 0.004 deg, specks under 0.0003 sq deg dropped, coordinates rounded to 4 decimals): 469k to 162k vertices, 20 MB to 3 MB (680 KB gzipped). The detailed file is kept as `madagascar_travel_time_bands_attributed.geojson`. GeoJSON gzipped and uploaded to `s3://<bucket>/data/` with `Content-Type: application/geo+json`, `Content-Encoding: gzip`.
4. `site/index.html` (MapLibre GL JS) uploaded to `s3://<bucket>/site/`; CloudFront serves both.
5. The Location API key goes in `site/config.js` (copy `site/config.example.js`; the key is public by design, so restrict it to your domain and the map actions).

## Caveats
- Road data in the source has not been validated.
- Health sites were filtered to those likely to offer child-focused services.
- Facility dots are not the same sites used to compute travel time.
- Bands are simplified polygons, so small features are generalised.

## Status
Live and tested in the built-in browser (desktop and phone width). The Amazon Location API key (`madagascar-map-key`, actions GetTile and GetStaticMap, Maps default provider) is restricted to the CloudFront domain as referrer. Base map: Amazon Location Standard style (attribution: AWS, HERE).

## Reproduce it
1. Convert the raster to four bands. This was done interactively with rasterio and shapely and is not included as a script: downsample 4x, polygonise (under 1 h, 1-2 h, 2-4 h, over 4 h), simplify at 0.002 degrees. Download the raster from HDX.
2. `python3 scripts/lighten_bands.py in.geojson out.geojson 0.004 0.0003` shrinks the bands for the web.
3. `python3 scripts/extract_health_facilities.py madagascar-latest.osm.pbf out.geojson` (needs `pip install osmium`) pulls health facilities from a Geofabrik extract.
4. Create a private S3 bucket (block public access, encryption on), upload `data/` and `site/`, put CloudFront with Origin Access Control in front, and create an Amazon Location API key (GetTile, GetStaticMap) restricted to the CloudFront domain. Put the key in `site/config.js`.

## Licences
Data: travel time CC BY 4.0 (Data for Children Collaborative); facilities ODbL 1.0 (OpenStreetMap contributors). Code: MIT (see `LICENSE`). The data keeps its own licences above.
