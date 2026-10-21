import copy
from contextlib import redirect_stdout
import importlib.machinery
import importlib.util
import json
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import io

MODULE = Path(__file__).resolve().parents[1] / 'script/osm-bookcases'
loader = importlib.machinery.SourceFileLoader('osm_bookcases', str(MODULE))
spec = importlib.util.spec_from_loader(loader.name, loader)
osm = importlib.util.module_from_spec(spec)
loader.exec_module(osm)
FIXTURES = Path(__file__).parent / 'fixtures'


class BookcasesTest(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads((FIXTURES / 'osm.json').read_text())
        self.locations, self.placemarks = osm.read_kml((FIXTURES / 'libraries.kml').read_bytes())

    def test_haversine(self):
        self.assertEqual(osm.distance((0, 0), (0, 0)), 0)
        self.assertAlmostEqual(osm.distance((0, 0), (0, 1)), 111194.9266, places=3)
        self.assertAlmostEqual(osm.distance((0, 0), (0, 180)), math.pi * 6371000)

    def test_nested_kml_coordinate_order_and_distinct_records(self):
        self.assertEqual(self.placemarks, 3)
        self.assertEqual(len(self.locations), 2)
        self.assertEqual(self.locations[0]['name'], 'Fixture & books')
        self.assertEqual(self.locations[0]['lat'], 37.87)
        self.assertEqual(self.locations[0]['lon'], -122.27)
        self.assertNotEqual(self.locations[0]['key'], self.locations[1]['key'])

    def test_types_tags_centers_and_identity(self):
        records = osm.read_osm(self.payload)
        self.assertEqual([r['osm_id'] for r in records], ['node/1', 'relation/2', 'way/1'])
        self.assertEqual(records[0]['tags']['access'], 'private')
        self.assertEqual(records[0]['version'], 3)
        self.assertEqual(records[2]['position_kind'], 'bounding-box center')
        self.assertEqual(records[0]['source_url'], 'https://www.openstreetmap.org/node/1')

    def test_bands_use_unrounded_distances_and_all_neighbors(self):
        base = osm.read_osm(self.payload)[0]
        for meters, expected in [(0, 'within-20m'), (19.99, 'within-20m'),
                                 (20.01, 'within-100m'), (99.99, 'within-100m'),
                                 (100.01, 'potential-addition')]:
            record = dict(base, lat=37.87 + math.degrees(meters / 6371000))
            row = osm.compare([record], self.locations)[0]
            self.assertEqual(row['review_band'], expected)
            self.assertFalse(row['identity_confirmed'])
            self.assertEqual(len(row['existing_within_100m']), 0 if meters > 100 else 2)
            self.assertEqual(row['nearest_existing']['key'], self.locations[0]['key'])

    def test_osm_peers_are_hints_not_deduplicated(self):
        first = osm.read_osm(self.payload)[0]
        rows = osm.compare([first, dict(first, osm_id='way/9')], self.locations)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['osm_within_20m'][0]['osm_id'], 'way/9')

    def test_partial_malformed_or_duplicate_osm_fails(self):
        bad = [dict(self.payload, remark='runtime timeout'), {},
               dict(self.payload, elements=self.payload['elements'] * 2)]
        for field, value in [('lat', None), ('lat', float('nan')), ('lon', 181), ('lat', True)]:
            payload = copy.deepcopy(self.payload)
            payload['elements'][0][field] = value
            bad.append(payload)
        payload = copy.deepcopy(self.payload)
        del payload['elements'][1]['center']
        bad.append(payload)
        for payload in bad:
            with self.assertRaises(ValueError):
                osm.read_osm(payload)

    def test_empty_result_and_outside_center_are_explicit(self):
        self.assertEqual(osm.read_osm({'elements': []}), [])
        self.payload['elements'][1]['center']['lat'] = 38
        self.assertFalse(osm.read_osm(self.payload)[2]['center_in_bounds'])
        with self.assertRaises(ValueError):
            osm.read_kml(b'<kml/>')

    def test_fetch_preserves_old_snapshot_on_partial_or_oversized_response(self):
        for raw in [b'{"elements": [], "remark": "runtime timeout"}', b'x' * 4_000_001]:
            with tempfile.TemporaryDirectory() as directory:
                target = Path(directory) / 'snapshot.json'
                target.write_text('previous snapshot')
                with patch.object(osm.urllib.request, 'urlopen', return_value=io.BytesIO(raw)):
                    with self.assertRaises(ValueError):
                        osm.fetch_snapshot(target)
                self.assertEqual(target.read_text(), 'previous snapshot')

    def test_offline_report_is_deterministic_and_preserves_provenance(self):
        snapshot = {'query': osm.QUERY, 'bounds_south_west_north_east': osm.BOUNDS,
                    'fetched_at': '2026-01-01T01:00:00Z', 'endpoint': osm.ENDPOINT,
                    'response': self.payload}
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            source = output / 'snapshot.json'
            osm.write_json(source, snapshot)
            with redirect_stdout(io.StringIO()):
                osm.analyze(source, FIXTURES / 'libraries.kml', output)
            before = (output / 'report.json').read_bytes()
            with redirect_stdout(io.StringIO()):
                osm.analyze(source, FIXTURES / 'libraries.kml', output)
            self.assertEqual(before, (output / 'report.json').read_bytes())
            report = json.loads(before)
            self.assertEqual(report['osm_count'], 3)
            self.assertEqual(report['query'], osm.QUERY)
            self.assertEqual(report['records'][0]['tags']['access'], 'private')
            snapshot['query'] = 'different bounds'
            osm.write_json(source, snapshot)
            with self.assertRaises(ValueError):
                osm.analyze(source, FIXTURES / 'libraries.kml', output)


if __name__ == '__main__':
    unittest.main()
