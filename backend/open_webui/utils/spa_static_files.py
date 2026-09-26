from pathlib import Path

from starlette.exceptions import HTTPException
from starlette.staticfiles import StaticFiles


class SPAStaticFiles(StaticFiles):
    def file_response(self, full_path, stat_result, scope, status_code=200):
        response = super().file_response(full_path, stat_result, scope, status_code)
        path = Path(full_path)
        if path.suffix == '.html' or path.name == 'version.json':
            # Revalidate the app shell before reusing references to a previous build.
            # Apply this after conditional handling so 304 responses carry it too.
            response.headers['Cache-Control'] = 'no-cache'
        return response

    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except HTTPException as ex:
            if ex.status_code != 404 or path.endswith('.js'):
                raise
            return await super().get_response('index.html', scope)
