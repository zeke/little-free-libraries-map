# OpenStreetMap public-bookcase spike

This is a separate review dataset, not input to the live map or the candidate-photo importer. No identities or additions have been approved. Start with [the review table](report.md); [report.json](report.json) retains full tags, links, all KML neighbors within 100 m, nearest KML point, nearby OSM peers, and provenance. [snapshot.json](snapshot.json) retains the complete Overpass JSON response and the request metadata.

## Observed results

Fetched on 2026-10-21 at 00:11:35 UTC, with OSM database timestamp 00:10:27 UTC:

| Observation                         | Count |
| ----------------------------------- | ----- |
| Imported KML placemarks / points     | 1,115 |
| OSM public-bookcase objects          | 299   |
| Within 20 m of a KML point           | 191   |
| Over 20 m, within 100 m              | 30    |
| No KML point within 100 m            | 78    |
| OSM objects with another within 20 m | 7     |

All 299 observed objects are nodes. One has multiple KML points within 20 m. None has an `access` tag; absence does not establish public access. These counts describe this snapshot, not complete real-world coverage.

The 191 close matches and 30 broader matches are uncertain identity candidates. The 78 potential additions are a field-review queue, not confirmed missing libraries. The original EXIF review script uses the same 6,371,000 m Haversine radius and 20 m candidate threshold. This spike adds an explicit 100 m broader-review band to expose coordinate discrepancies instead of assuming everything beyond 20 m is new. Neither threshold is calibrated ground truth. Distances use unrounded values for classification; JSON exports meters to six decimal places to avoid macOS/Linux floating-point serialization differences. That precision does not imply coordinate accuracy.

Examples for review:

- [node/10556462196](https://www.openstreetmap.org/node/10556462196): nearest imported point, 1346 Grizzly Peak Blvd, is 217.2 m away. Potential addition requiring a site check.
- [node/10648462715](https://www.openstreetmap.org/node/10648462715): 106.3 m from 1045 Peralta Ave, just beyond the broad threshold. Shows why the potential-addition label is tentative.
- [node/10139164051](https://www.openstreetmap.org/node/10139164051): 62.0 m from 1935 Berryman St. Could be a different bookcase or displaced coordinates.
- [node/10139119185](https://www.openstreetmap.org/node/10139119185): 4.0 m from 735 The Alameda. Close, but still requires matching address, appearance, or independent field evidence.

## Scope and provenance

Bounds are south 37.80, west -122.34, north 37.94, east -122.20. This rectangle covers Berkeley, Albany, El Cerrito and part of north Oakland, not administrative boundaries or the entire East Bay. Compare against every existing KML point, including points outside the query rectangle, to avoid artificial edge mismatches.

The [documented public-bookcase tag](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dpublic_bookcase) is the sole selector. It includes community book exchanges regardless of affiliation with Little Free Library. It misses untagged bookcases, alternate tags, removed amenities, and anything outside the rectangle. Do not infer absence from OSM absence.

The exact [Overpass QL](https://wiki.openstreetmap.org/wiki/Overpass_API/Overpass_QL) query, endpoint, bounds, UTC fetch time and OSM base time are stored with the snapshot/report:

```overpass
[out:json][timeout:60];
nwr["amenity"="public_bookcase"](37.80,-122.34,37.94,-122.20);
out meta center;
```

Each report row keeps `node/ID`, `way/ID` or `relation/ID`, an OSM source URL, complete tags, version and edit timestamp where returned. For ways/relations, `out center` returns a bounding-box center, not an entrance or necessarily a point inside the geometry or rectangle. The report marks that position kind and whether the center is inside the bounds. Nearby OSM objects are retained separately even if they might represent the same physical bookcase.

The report records SHA-256 hashes of the snapshot file and input KML. KML neighbor keys are one-based placemark/point ordinals in that exact hashed file, not persistent external IDs. Nested folders and multiple points are supported; lines/polygons are not treated as library points. Malformed point coordinates fail the run rather than silently lowering the baseline count. No original imported data was refreshed or changed for this comparison.

## Reproduce

Run from the repository root on macOS or Linux with Python 3.9+:

```sh
./script/test
./script/osm-bookcases compare
# The checked-in report is reproduced offline, byte for byte:
git diff --exit-code -- osm/report.json osm/report.md
```

No package installation, API key, geocoder, image classifier or imagery request is needed. `script/test` covers Haversine distances and threshold boundaries, nested KML, all OSM element types, overlapping records, incomplete/error responses, malformed coordinates and deterministic offline reporting. The tiny synthetic fixtures are in `tests/fixtures/`. No linter or typechecker was configured in the baseline repo.

To fetch a current snapshot deliberately (this overwrites the local research snapshot, and live counts can change):

```sh
./script/osm-bookcases fetch
./script/osm-bookcases compare
./script/test
```

On this Mac Mini, Apple's `/usr/bin/python3` 3.9.6 failed the public endpoint TLS handshake. The installed Homebrew Python 3.15 succeeded with certificate verification enabled:

```sh
/opt/homebrew/bin/python3 script/osm-bookcases fetch
./script/osm-bookcases compare
```

The fetch is one bounded HTTPS POST, with a 60-second server timeout, 90-second client timeout, descriptive User-Agent and a 4 MB response cap. HTTP errors and Overpass `remark` responses fail before replacing the snapshot. No automatic retries or fallback services are used; wait and rerun manually if the public service is busy. For a new snapshot without replacing this one, use `fetch --snapshot /tmp/bookcases.json`, then `compare --snapshot /tmp/bookcases.json --output /tmp` (the output directory must exist). Live refetches are not historical reproductions; the committed snapshot is the reproducible input.

## Licensing and review limitations

© OpenStreetMap contributors. The OSM extract and OSM-derived data are available under the [Open Database License 1.0](https://opendatacommons.org/licenses/odbl/1-0/); see [OSM's copyright and attribution notice](https://www.openstreetmap.org/copyright). Preserve this attribution, source links, and license notice when redistributing the data or displaying a review interface.

ODbL sections 4.2–4.6 cover notices, share-alike and access to derivative databases. Public use of an adapted OSM database can require offering that database or its alterations under ODbL; produced works also require attribution. Keeping files separate is a provenance boundary, not an automatic exemption from those obligations. The imported Berkeley dataset has separate provenance and its README does not establish permission to relicense it. Resolve compatibility and the intended collective/derivative database arrangement before any merged publication. This spike does not assign a new license to the original KML or establish that the map's current tile attribution suffices for future OSM-derived location data.

For each candidate, inspect tags, edit age, OSM peers, and all nearby KML records, then independently verify physical location, identity, current existence and access. Coordinate errors, moved/removed bookcases, multiple bookcases on one parcel, ambiguous names and incomplete tags can defeat proximity matching. There is no automated acceptance, conflation, map update, OSM edit, Street View workflow or classifier integration.
