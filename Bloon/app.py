from .routes import RouteManager
from .http.http import ErrorResponse
from pathlib import Path
from .settings import SettingsLoader
import uvicorn
import pprint
import os


class App:
    def __init__(self, project_level):
        """
        Init. Application
        :param project_level: Use __name__ to do this.
        """
        self.routes = RouteManager()
        self.project_level = project_level
        self.working_directory = Path(os.getcwd())
        self.settings = SettingsLoader(os.getcwd())

    async def __call__(self, scope, receive, send):
        """
        ASGI Handler.
        :param scope:
        :param receive:
        :param send:
        :return:
        """
        assert scope["scheme"] in ["http", "https"]

        pprint.pprint(scope)

        # Get Resp.
        resp = self.routes.get_node(route=scope["path"])

        if resp is None:
            return
        else:
            resp = await resp()

        print(resp.head(), resp.body_(), sep="\n")

        await send(resp.head())
        await send(resp.body_())

    def run(self, host: str = "localhost", port: int = 8000, **config):
        """
        Run by uvicorn.
        :param host:
        :param port:
        :param config:
        :return:
        """
        uvicorn.run(self, host=host, port=port, access_log=False, **config)

    def route(self, app_name, route, **conf):
        def decorator(f):
            self.routes.register(as_parent=False, key=route, value=f, app_name=app_name)
        return decorator
