"""Run with: python -m unittest discover -s backend/tests -p test_spa_static_files.py"""

import sys
import tempfile
import unittest
from pathlib import Path

from starlette.applications import Starlette
from starlette.routing import Mount
from starlette.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from open_webui.utils.spa_static_files import SPAStaticFiles


class SPAStaticFilesTest(unittest.TestCase):
    def test_deployment_cache_policy(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            index = root / 'index.html'
            index.write_text('<script src="/_app/immutable/old.js"></script>', encoding='utf-8')
            assets = root / '_app' / 'immutable'
            assets.mkdir(parents=True)
            (assets / 'old.js').write_text('/* old build */', encoding='utf-8')
            (assets / 'app.css').write_text('body {}', encoding='utf-8')
            (root / '_app' / 'version.json').write_text('{"version":"old"}', encoding='utf-8')
            app = Starlette(routes=[Mount('/', SPAStaticFiles(directory=root, html=True))])

            with TestClient(app) as client:
                for url in ('/', '/index.html', '/c/existing-chat', '/_app/version.json'):
                    response = client.get(url)
                    self.assertEqual(response.status_code, 200)
                    self.assertEqual(response.headers.get('cache-control'), 'no-cache')
                    cached = client.get(url, headers={'If-None-Match': response.headers['etag']})
                    self.assertEqual(cached.status_code, 304)
                    self.assertEqual(cached.headers.get('cache-control'), 'no-cache')
                    self.assertEqual(client.head(url).headers.get('cache-control'), 'no-cache')

                for url in ('/_app/immutable/old.js', '/_app/immutable/app.css'):
                    response = client.get(url)
                    self.assertEqual(response.status_code, 200)
                    self.assertNotIn('cache-control', response.headers)

                old_etag = client.get('/').headers['etag']
                index.write_text('<script src="/_app/immutable/new-build.js"></script>', encoding='utf-8')
                (assets / 'old.js').unlink()
                (assets / 'new-build.js').write_text('/* new build */', encoding='utf-8')
                response = client.get('/', headers={'If-None-Match': old_etag})
                self.assertEqual(response.status_code, 200)
                self.assertIn('new-build.js', response.text)
                self.assertEqual(response.headers.get('cache-control'), 'no-cache')
                self.assertEqual(client.get('/_app/immutable/new-build.js').status_code, 200)
                self.assertEqual(client.get('/_app/immutable/old.js').status_code, 404)
                self.assertEqual(client.post('/c/existing-chat').status_code, 405)


if __name__ == '__main__':
    unittest.main()
