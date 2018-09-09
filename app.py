import aiohttp_debugtoolbar
from aiohttp import web
from aiohttp_utils import negotiation
from umongo.exceptions import NoDBDefinedError
from aiojobs.aiohttp import setup as setup_scheduler

from api import routes
from api.middleware_app import error_middleware, auth_middleware
import settings


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')

async def synchronize_indexes():
    from models.main import instance

    for model in instance._doc_lookup:
        document = instance.retrieve_document(model)
        try:
            await document.collection.drop_indexes()
        except NoDBDefinedError:
            pass

        await document.ensure_indexes()


def create_app(argv) -> web.Application:
    """App factory. Sets up routes and all plugins.
    """
    middle = [
        # error_middleware,
        auth_middleware,
    ]

    if settings.DEBUG:
        middle.append(aiohttp_debugtoolbar.middleware)

    app = web.Application(middlewares=middle, debug=settings.DEBUG)
    app['websockets'] = []
    if settings.DEBUG:
        aiohttp_debugtoolbar.setup(app)

    app.on_shutdown.append(on_shutdown)

    # Set up routes
    routes.setup(app)
    # Use content negotiation middleware to render JSON responses
    negotiation.setup(app)

    from models.main import client, db
    app.client = client
    app.db = db
    app.synchronize_indexes = synchronize_indexes

    setup_scheduler(app)
    return app
