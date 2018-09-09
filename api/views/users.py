from datetime import datetime
from bson import ObjectId

from aiohttp import web

from models.user import User, UserRelationship
from api.middleware_view import jwt_required, not_authenticated

from exceptions import (
    Ok,
    InvalidUserId,
    UserAlreadyBlocked,
    NoSuchUser,
    UnblockUnblockedUser,
)


class BlockUser(web.View):

    @jwt_required()
    async def post(self, **kw):
        me = self.request.user
        user_id = self.request.match_info.get('user_id', None)

        if not ObjectId.is_valid(user_id):
            raise InvalidUserId

        user = await User.find_one({'_id': ObjectId(user_id)})
        if user is None:
            raise NoSuchUser

        users_relationship = await UserRelationship.find_one({
            '$or': [
                {'from_user': ObjectId(me.pk), 'to_user': ObjectId(user_id)},
                {'from_user': ObjectId(user_id), 'to_user': ObjectId(me.pk)},
            ]
        })

        if users_relationship is not None:
            if users_relationship['status'] == 'blocked':
                raise UserAlreadyBlocked
            users_relationship.from_user = me.pk
            users_relationship.to_user = user.pk
            users_relationship.status = 'blocked'
        else:
            users_relationship = UserRelationship(
                from_user=me.pk,
                to_user=user.pk,
                status='blocked',
                date=datetime.utcnow()
            )

        await users_relationship.commit()
        raise Ok


class UnblockUser(web.View):

    @jwt_required()
    async def post(self, **kw):
        me = self.request.user
        user_id = self.request.match_info.get('user_id', None)

        if not ObjectId.is_valid(user_id):
            raise InvalidUserId

        user = await User.find_one({'_id': ObjectId(user_id)})
        if user is None:
            raise NoSuchUser

        user_blocked_relationship = await UserRelationship.find_one(
            {
                'from_user': ObjectId(me.pk),
                'to_user': ObjectId(user_id),
                'status': 'blocked',
            })

        if user_blocked_relationship is not None:
            await UserRelationship.collection.delete_one({'_id': ObjectId(user_blocked_relationship.pk)})
            raise Ok
        else:
            raise UnblockUnblockedUser


class SuggestUserToContacts(web.View):

    @jwt_required()
    async def post(self, **kw):
        me = self.request.user
        user_id = self.request.match_info.get('user_id', None)

        raise Ok
