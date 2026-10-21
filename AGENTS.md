# Project guidance

Keep this file current when meaningful changes affect the scripts, data boundaries, or checks.

- The site is static HTML/Leaflet with no build step. `libraries.kml` is externally maintained, read-only imported data. Follow `.claude/CLAUDE.md`; do not hand-edit it.
- Photo candidates use `script/analyze-candidates`, `exiftool`, existing `xml2js`, and the review gallery in `candidates/index.html`. Its 20 m distance check flags potential duplicates, not verified identities.
- OSM research stays in `osm/`, separate from the published map and candidate-photo importer. Read `osm/README.md` for provenance, licensing, results, and exact commands. Do not automatically import it into KML, the map, or OSM.
- Run `./script/test` for the offline OSM algorithm/fixture suite (Python 3.9+, no added packages). No linter or typechecker is configured. Run `./script/osm-bookcases compare` to regenerate the checked-in report from its snapshot and KML.
- `.github/workflows/test.yml` runs offline checks on pushes and PRs. `deploy.yml` deploys only pushes to `main`; do not deploy as part of the spike.
