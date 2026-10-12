"""Path/retention regressions using new fixtures, never historical GIS data.

Run with the shared installed Python (-I -B). Optional environment:
ACCESSIBILITAT_REVIEW_REF selects an immutable Git version for old-failure proof;
ACCESSIBILITAT_QGIS_CLIENT enables the public CLI's read-only YAML validation.
Fixture files and evidence remain under ignored sandbox, with a new run per call.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import types
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[2]
REVIEW_REF = os.environ.get('ACCESSIBILITAT_REVIEW_REF')
if REVIEW_REF and not re.fullmatch(r'[0-9a-f]{40}', REVIEW_REF):
    raise ValueError('Use an exact immutable review commit')
SCRIPT = 'practiques/accessibilitat-vilaseca/preparar.py'
OLD_START = 'tmp/dades-docents/qgis/accessibilitat-vilaseca-20261006-inici'
OLD_GUIDE = 'tmp/dades-docents/qgis/accessibilitat-vilaseca-20261007-guies'
FIXTURES = ROOT / 'sandbox/practiques/accessibilitat-vilaseca' / (
    'capture-config-regression-33-' + str(time.time_ns()))


def source_text(path):
    if REVIEW_REF:
        return subprocess.run(
            ['git', 'show', REVIEW_REF + ':' + path], cwd=ROOT,
            check=True, capture_output=True, text=True).stdout
    return (ROOT / path).read_text()


def load_preparer():
    module = types.ModuleType('accessibilitat_capture_fixture')
    module.__file__ = str(ROOT / SCRIPT)
    exec(compile(source_text(SCRIPT), module.__file__, 'exec'), module.__dict__)
    return module


class CaptureConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        parent = ROOT.resolve() / 'sandbox/practiques/accessibilitat-vilaseca'
        if FIXTURES.parent.resolve() != parent:
            raise ValueError('Fixture parent escapes the source-only sandbox.')
        FIXTURES.mkdir(parents=True)

    def setUp(self):
        self.root = FIXTURES / self._testMethodName / 'consumer with spaces'
        self.out = self.root / 'sandbox/practiques/accessibilitat-vilaseca/new-run'
        self.captures = self.out / 'captures'
        self.captures.mkdir(parents=True)
        (self.out / '.owner.json').write_text(json.dumps({'owner': 'preparar.py'}))
        self.preparer = load_preparer()
        self.preparer.ROOT, self.preparer.OUT = self.root, self.out
        (self.root / 'context/qgis').mkdir(parents=True)
        (self.root / 'context/qgis/accessibilitat-inici.md').write_text(
            '# Synthetic path-only fixture\n')
        geojson = json.dumps({'type': 'FeatureCollection', 'features': []})
        (self.out / 'alumnat').mkdir()
        (self.out / 'alumnat/points.geojson').write_text(geojson)
        # This is a marker for a connection-path assertion, not GIS validity proof.
        (self.out / 'alumnat/input.gpkg').write_text('synthetic path fixture\n')
        (self.out / 'docent').mkdir()
        (self.out / 'docent/points.geojson').write_text(geojson)
        (self.root / 'tmp/fixture-data').mkdir(parents=True)
        (self.root / 'tmp/fixture-data/shared.geojson').write_text(geojson)
        self.recipe = {
            'id': 'accessibilitat-inici', 'title': 'Synthetic path fixture',
            'source_prompt': 'context/qgis/accessibilitat-inici.md',
            'runtime': {'display_backend': 'x11', 'locale': 'ca'},
            'plugins': ['processing'],
            'data': [{'id': 'points', 'type': 'vector',
                      'path': 'accessibilitat-vilaseca-20261006-inici/alumnat/points.geojson'}],
            'connections': [{'id': 'input', 'type': 'gpkg', 'name': 'fixture',
                             'path': OLD_START + '/alumnat/input.gpkg'}],
            'setup': [{'action': 'load_vector', 'path': OLD_START + '/alumnat/points.geojson',
                       'name': 'Fixture points'}],
            'captures': [self.capture('inici', OLD_START),
                         self.capture('resultat', OLD_GUIDE)],
        }
        self.base_config = {
            'runtime': {'default_image': 'sha256:' + '0' * 64,
                        'display_backend': 'offscreen', 'pull_policy': 'explicit'},
            'paths': {'recipes': ['context/qgis/accessibilitat-inici.yml'],
                      'data_root': 'tmp/fixture-data', 'output_root': 'tmp/fixture-captures',
                      'cache_root': 'tmp/fixture-cache', 'play_prompts': 'context/qgis',
                      'director_plans': 'tmp/fixture-plans', 'plays': 'tmp/fixture-plays'},
            'plugins': ['processing'],
            'data': [{'id': 'shared', 'type': 'vector', 'path': 'shared.geojson'}],
        }
        self.write_inputs()

    @staticmethod
    def capture(name, prefix):
        return {
            'id': name, 'mode': 'window', 'target': {'object_name': 'QgisApp'},
            'steps': [{'action': 'load_vector',
                       'path': prefix + '/docent/points.geojson|layername=fixture',
                       'name': 'Fixture layer'}, {'action': 'clear_message_bar'}],
            'drawings': [],
            'output': {'path': prefix + '/captures/' + name + '.png',
                       'annotations_svg': prefix + '/captures/' + name + '.annotations.svg',
                       'manifest': prefix + '/captures/' + name + '.manifest.yml'},
        }

    def write_inputs(self):
        (self.root / 'context/qgis/accessibilitat-inici.yml').write_text(
            yaml.safe_dump(self.recipe, allow_unicode=True, sort_keys=False))
        (self.root / '.unaltracaptura-qgis.yml').write_text(
            yaml.safe_dump(self.base_config, allow_unicode=True, sort_keys=False))

    def generate(self):
        self.preparer.capture_config()
        config = yaml.safe_load((self.captures / 'config.yml').read_text())
        recipe_path = Path(config['paths']['recipes'][0])
        if not recipe_path.is_absolute():
            recipe_path = self.captures / recipe_path
        self.assertTrue(recipe_path.is_file(), 'Provider cannot discover the derived recipe')
        return config, yaml.safe_load(recipe_path.read_text())

    def test_historical_recipe_is_not_in_the_normal_registry(self):
        config = yaml.safe_load(source_text('.unaltracaptura-qgis.yml'))
        self.assertNotIn('context/qgis/accessibilitat-inici.yml', config['paths']['recipes'])

    def test_recipe_inputs_and_scene_uris_resolve_from_config_parent(self):
        config, recipe = self.generate()
        data_root = Path(config['paths']['data_root'])
        if not data_root.is_absolute():
            data_root = self.captures / data_root
        data_path = Path(recipe['data'][0]['path'])
        if not data_path.is_absolute():
            data_path = data_root / data_path
        self.assertEqual(data_path.resolve(), self.out / 'alumnat/points.geojson')
        self.assertTrue(data_path.is_file())
        self.assertEqual(recipe['connections'][0]['path'], str(self.out / 'alumnat/input.gpkg'))
        self.assertEqual(recipe['setup'][0]['path'], str(self.out / 'alumnat/points.geojson'))
        self.assertEqual(recipe['captures'][1]['steps'][0]['path'],
                         str(self.out / 'docent/points.geojson') + '|layername=fixture')
        self.assertEqual(Path(recipe['source_prompt']),
                         self.root / 'context/qgis/accessibilitat-inici.md')
        shared = Path(config['data'][0]['path'])
        if not shared.is_absolute():
            shared = data_root / shared
        self.assertEqual(shared.resolve(), self.root / 'tmp/fixture-data/shared.geojson')

    def test_outputs_are_new_and_confined_and_copied_captures_stay_intact(self):
        copied = self.captures / 'inici.png'
        copied.write_bytes(b'copied capture witness')
        before = hashlib.sha256(copied.read_bytes()).hexdigest()
        config, recipe = self.generate()
        output_root = self.captures / 'rendered'
        self.assertEqual(Path(config['paths']['output_root']), output_root)
        destinations = []
        for capture in recipe['captures']:
            for key, value in capture['output'].items():
                path = Path(value)
                self.assertTrue(path.is_absolute())
                self.assertTrue(path.is_relative_to(output_root))
                self.assertFalse(path.exists())
                destinations.append(path)
        self.assertEqual(len(destinations), len(set(destinations)))
        for key in ['cache_root', 'director_plans', 'plays']:
            self.assertTrue(Path(config['paths'][key]).is_relative_to(self.out))
        self.assertEqual(hashlib.sha256(copied.read_bytes()).hexdigest(), before)
        self.assertEqual(recipe['runtime'], self.recipe['runtime'])
        self.assertEqual(recipe['captures'][0]['target'], self.recipe['captures'][0]['target'])

    def test_second_derivation_refuses_to_overwrite_metadata(self):
        self.generate()
        before = {p: p.read_bytes() for p in [self.captures / 'recipe.yml', self.captures / 'config.yml']}
        with self.assertRaises((AssertionError, ValueError, FileExistsError)):
            self.preparer.capture_config()
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_existing_render_output_is_not_reused(self):
        rendered = self.captures / 'rendered'
        rendered.mkdir()
        witness = rendered / 'inici.png'
        witness.write_bytes(b'author output')
        with self.assertRaises((AssertionError, ValueError, FileExistsError)):
            self.preparer.capture_config()
        self.assertEqual(witness.read_bytes(), b'author output')
        self.assertFalse((self.captures / 'recipe.yml').exists())

    def test_sealed_run_is_refused_before_writing(self):
        (self.out / 'sealed.json').write_text('{}')
        with self.assertRaises((AssertionError, ValueError)):
            self.preparer.capture_config()
        self.assertFalse((self.captures / 'recipe.yml').exists())

    def test_symlink_output_escape_is_refused(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (self.captures / 'rendered').symlink_to(outside, target_is_directory=True)
        with self.assertRaises((AssertionError, ValueError)):
            self.preparer.capture_config()
        self.assertFalse((self.captures / 'recipe.yml').exists())
        self.assertEqual(list(outside.iterdir()), [])

    def test_input_traversal_is_refused(self):
        self.recipe['setup'][0]['path'] = OLD_START + '/../../../../outside.gpkg'
        self.write_inputs()
        with self.assertRaises((AssertionError, ValueError)):
            self.preparer.capture_config()
        self.assertFalse((self.captures / 'recipe.yml').exists())

    def test_input_symlink_escape_is_refused(self):
        outside = self.root / 'outside.geojson'
        outside.write_text('{"type":"FeatureCollection","features":[]}')
        link = self.out / 'alumnat/link.geojson'
        link.symlink_to(outside)
        self.recipe['setup'][0]['path'] = OLD_START + '/alumnat/link.geojson'
        self.write_inputs()
        with self.assertRaises((AssertionError, ValueError)):
            self.preparer.capture_config()
        self.assertFalse((self.captures / 'recipe.yml').exists())

    def test_all_twelve_template_captures_keep_parameters_and_new_destinations(self):
        # Only versioned YAML text is read; no historical GIS inputs are used.
        self.recipe = yaml.safe_load(source_text('context/qgis/accessibilitat-inici.yml'))
        self.write_inputs()
        _, derived = self.generate()
        self.assertEqual(len(derived['captures']), 12)

        def non_path_fields(value):
            if isinstance(value, dict):
                return {k: non_path_fields(v) for k, v in value.items()
                        if k not in {'path', 'source_prompt', 'annotations_svg', 'manifest'}}
            if isinstance(value, list):
                return [non_path_fields(v) for v in value]
            return value

        self.assertEqual(non_path_fields(derived), non_path_fields(self.recipe))
        outputs = [Path(value) for capture in derived['captures']
                   for value in capture['output'].values()]
        self.assertEqual(len(outputs), 36)
        self.assertEqual(len(set(outputs)), 36)
        self.assertTrue(all(p.is_relative_to(self.captures / 'rendered') for p in outputs))
        self.assertTrue(all(not p.exists() for p in outputs))

    def test_wrong_run_root_is_refused(self):
        self.preparer.OUT = self.root / 'tmp/other-run'
        (self.preparer.OUT / 'captures').mkdir(parents=True)
        (self.preparer.OUT / '.owner.json').write_text(json.dumps({'owner': 'preparar.py'}))
        with self.assertRaises((AssertionError, ValueError)):
            self.preparer.capture_config()
        self.assertFalse((self.preparer.OUT / 'captures/recipe.yml').exists())

    def test_precaption_teacher_digest_is_well_formed(self):
        text = source_text('context/practice-retention-inventory.md')
        row = next(line for line in text.splitlines()
                   if line.startswith('| Lectura docent abans de captions'))
        digest = re.findall(r'`([^`]+)`', row)[0]
        self.assertRegex(digest, r'^[0-9a-f]{64}$')

    def test_public_cli_validates_the_new_fixture_readonly(self):
        client = os.environ.get('ACCESSIBILITAT_QGIS_CLIENT')
        if not client:
            self.skipTest('Public CLI selection must be supplied explicitly')
        self.generate()
        before = {p: p.read_bytes() for p in [self.captures / 'recipe.yml', self.captures / 'config.yml']}
        env = dict(os.environ)
        for key in ['DOCKER_CONTEXT', 'DOCKER_TLS_VERIFY', 'DOCKER_CERT_PATH', 'DOCKER_API_VERSION',
                    'UNALTRACAPTURA_QGIS_PROJECT_ID', 'UNALTRACAPTURA_QGIS_JOB_REGISTRY',
                    'UNALTRACAPTURA_QGIS_JOB_REGISTRY_HOST', 'UNALTRACAPTURA_QGIS_JOB_GRANT']:
            env.pop(key, None)
        env.update({'DOCKER_HOST': 'unix:///var/run/docker.sock',
                    'MCP_CONSUMER_WORKSPACE': str(ROOT),
                    'UNALTRACAPTURA_QGIS_WORKSPACE': str(ROOT),
                    'UNALTRACAPTURA_QGIS_HOST_WORKSPACE': str(ROOT)})
        result = subprocess.run(
            [client, '-I', '-B', '-m', 'veure_qgis_mcp.cli', 'validate',
             '--config', str(self.captures / 'config.yml')],
            cwd=ROOT, env=env, capture_output=True, text=True, timeout=30)
        (self.root / 'provider-validation.json').write_text(json.dumps({
            'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}, indent=2))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(before, {p: p.read_bytes() for p in before})


if __name__ == '__main__':
    print('Retained new fixtures:', FIXTURES, flush=True)
    unittest.main(verbosity=2)
