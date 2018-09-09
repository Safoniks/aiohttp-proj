from collections import namedtuple

import aiohttp_cors
import settings

from api.views import (
    auth,
    me,
    users,
    utility,
)

Route = namedtuple('Route', ['method', 'path', 'handler', 'name'])

ROUTES = [
    Route('GET', '/registry/', handler=auth.Registry, name='test'),

    Route('GET', '/valid_invite_code/', handler=auth.ValidInviteCode, name='valid_invite_code'),
    Route('POST', '/login/', handler=auth.Login, name='login'),
    Route('POST', '/registry/', handler=auth.Registry, name='registry'),
    Route('POST', '/restore_password/', handler=auth.RestorePassword, name='restore_password'),
    Route('POST', '/get_invite_code/', handler=auth.GetInviteCode, name='get_invite_code'),

    Route('GET', '/tags/', handler=utility.GetTags, name='get_tags'),
    Route('GET', '/me/', handler=me.Me, name='me'),
    Route('GET', '/me/detailed/', handler=me.MeDetailed, name='me_detailed'),
    Route('POST', '/users/{user_id}/contacts/',
          handler=users.SuggestUserToContacts, name='send_contact_request'),
    Route('POST', '/users/{user_id}/block/',
          handler=users.BlockUser, name='block_user'),
    Route('POST', '/users/{user_id}/unblock/',
          handler=users.UnblockUser, name='unblock_user'),
]


def setup(app, url_prefix=''):
    """Set up routes. Enables CORS."""
    # Enable CORS for all routes
    cors = aiohttp_cors.setup(
        app,
        defaults={
            '*': aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers='*', allow_headers='*'
            )
        }
    )
    config = settings.ROUTES
    url_prefix = config.get('URL_PREFIX', url_prefix)
    app.router.add_static(settings.STATIC_URL, settings.STATIC_DIR, name='static')
    for route in ROUTES:
        method, url, handler, name = route
        full_url = '{prefix}/{url}'.format(prefix=url_prefix.rstrip('/'), url=url.lstrip('/'))
        cors.add(app.router.add_route(method, full_url, handler, name=name))
