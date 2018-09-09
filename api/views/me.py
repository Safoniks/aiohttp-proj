from aiohttp import web
from aiohttp_utils import Response
from api.serializers.input_serializers import (
    UserSchema,
)
from api.middleware_view import jwt_required, not_authenticated


class Me(web.View):

    @jwt_required()
    async def get(self, **kw):
        me = self.request.user
        output_fields = (
            'id',
            'email',
            'photo',
            'current_location',
            'personal_invite_code',
            'bubbles',
            'is_active',
            'is_notifications_enabled',
        )

        me_schema = UserSchema(strict=True, only=output_fields)
        data = me_schema.dump(me).data
        return Response(data)


class MeDetailed(web.View):

    @jwt_required()
    async def get(self, **kw):
        me = self.request.user
        me_schema = UserSchema(strict=True)
        data = me_schema.dump(me).data
        return Response(data)
