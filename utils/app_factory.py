import aiohttp_debugtoolbar
from aiojobs.aiohttp import setup as setup_scheduler
from aiohttp import web
from aiohttp_utils import negotiation
from umongo.exceptions import NoDBDefinedError

from api import routes
from api.middleware_app import error_middleware, auth_middleware
import settings


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def shutdown(server, app, handler):
    server.close()
    await server.wait_closed()
    app.client.close()  # database connection close
    await app.shutdown()
    await handler.shutdown(10.0)
    await app.cleanup()


async def setup_models(app):
    from models.main import client, db, instance

    for model in instance._doc_lookup:
        document = instance.retrieve_document(model)
        try:
            await document.collection.drop_indexes()
        except NoDBDefinedError:
            pass

        await document.ensure_indexes()

    app.client = client
    app.db = db

async def init(loop):
    middle = [
        error_middleware,
        auth_middleware,
    ]

    if settings.DEBUG:
        middle.append(aiohttp_debugtoolbar.middleware)

    app = web.Application(loop=loop, middlewares=middle, debug=settings.DEBUG)
    app['websockets'] = []
    if settings.DEBUG:
        aiohttp_debugtoolbar.setup(app)

    # Set up routes
    routes.setup(app)
    # Use content negotiation middleware to render JSON responses
    negotiation.setup(app)

    await setup_models(app)
    app.on_shutdown.append(on_shutdown)
    setup_scheduler(app)

    handler = app.make_handler()
    server = loop.create_server(handler, settings.HOST, settings.PORT)
    return server, handler, app
