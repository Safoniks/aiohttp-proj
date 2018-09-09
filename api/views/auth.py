from datetime import datetime, timedelta
import json
import jwt
from bson import ObjectId

from aiohttp import web
from aiohttp_utils import Response
from aiojobs.aiohttp import spawn

from models.user import User, UserRelationship
from models.other import InviteGroup, GetInviteCodeRequest
from models.utils import create_new_invite_code
from api.serializers.input_serializers import (
    register_user,
    InviteCodeSchema,
    UserSchema,
)
from api.middleware_view import jwt_required, not_authenticated
from api.background_tasks import send_email_in_background

from exceptions import (
    Ok,
    NoSuchUser,
    WrongPassword,
    NoMultipartFormData,
    NoSuchInviteCode,
    InviteGroupCodeLimitExpired,
    NotJSONData,
    UserAlreadyRegistered,
    GetInviteCodeProcessed,
    GetInviteCodeAccepted,
    GetInviteCodeRejected,
    NoGetParameters,
)

from utils.utils import generate_password, send_email
from settings import (
    JWT_SECRET,
    JWT_ALGORITHM,
    JWT_EXP_DELTA_DAYS,
    SENDER_EMAIL,
    GET_INVITE_CODE,
    RESTORE_PASSWORD,
)


class Login(web.View):

    @not_authenticated()
    async def post(self, **kw):
        try:
            json_data = await self.request.json()
        except (AssertionError, ValueError):
            raise NotJSONData
        login_schema = UserSchema(strict=True, only=('email', 'password'))
        data = login_schema.load(json_data).data

        user = await User.find_one({'email': data['email']})
        if not user:
            raise NoSuchUser
        if not user.check_password(data['password']):
            raise WrongPassword

        payload = {
            'user_id': str(user.id),
            'exp': datetime.utcnow() + timedelta(days=JWT_EXP_DELTA_DAYS)
        }
        jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
        return Response({'token': jwt_token.decode('utf-8')})


class ValidInviteCode(web.View):

    async def get(self, **kw):
        response = {
            'invited_type': '',
            'invited_by': '',
        }

        query = dict(self.request.query)
        if not query:
            raise NoGetParameters
        data = InviteCodeSchema(strict=True).load(query).data
        invite_code = data['invite_code']

        user = await User.find_one({'personal_invite_code': invite_code})
        if user is not None:
            response['invited_type'] = 'personal'
            response['invited_by'] = str(user.pk)
            return Response(response)

        group_code = await InviteGroup.find_one({'code': invite_code})
        if group_code is not None:
            if group_code.available_uses > 0:
                group_code.available_uses -= 1
                await group_code.commit()

                response['invited_type'] = 'group'
                response['invited_by'] = str(group_code.pk)
                return Response(response)
            else:
                raise InviteGroupCodeLimitExpired

        invite_code_request = await GetInviteCodeRequest.find_one({'code': invite_code})
        if invite_code_request is not None:
            response['invited_type'] = 'admin'
            response['invited_by'] = str(invite_code_request.pk)
            return Response(response)

        raise NoSuchInviteCode


class Registry(web.View):

    @not_authenticated()
    async def post(self, **kw):
        '''
        Content-Type: multipart/form-data
        Fields:
        1. 'photo' -> content_type='image/*' (file)
        2. 'json' -> content_type='application/json' (all data in json)
        :param kw:
        :return:
        '''
        try:
            form_data = await self.request.multipart()
        except (AssertionError, ValueError):
            raise NoMultipartFormData

        new_user = await register_user(form_data)
        if new_user.invited_type == 'personal':
            await UserRelationship(
                from_user=ObjectId(new_user.invited_by),
                to_user=new_user.pk,
                status='accepted',
                date=datetime.utcnow()
            ).commit()

        raise Ok


class RestorePassword(web.View):

    @not_authenticated()
    async def post(self, **kw):
        try:
            json_data = await self.request.json()
        except (AssertionError, ValueError):
            raise NotJSONData

        restore_password_schema = UserSchema(strict=True, only=('email', ))
        data = restore_password_schema.load(json_data).data
        email = data['email']

        user = await User.find_one({'email': email})
        if user is None:
            raise NoSuchUser

        password = generate_password()
        user.set_password(password)

        await user.commit()
        send_email(
            RESTORE_PASSWORD['mail']['text'].format(code=password),
            RESTORE_PASSWORD['mail']['subject'],
            SENDER_EMAIL,
            email
        )

        raise Ok


class GetInviteCode(web.View):

    @not_authenticated()
    async def post(self, **kw):
        try:
            json_data = await self.request.json()
        except (AssertionError, ValueError):
            raise NotJSONData

        get_invite_code_schema = UserSchema(strict=True, only=('email', ))
        data = get_invite_code_schema.load(json_data).data
        email = data['email']

        user = await User.find_one({'email': email})
        if user:
            raise UserAlreadyRegistered

        get_invite_code_request = await GetInviteCodeRequest.find_one({'email': email})
        if get_invite_code_request:
            if get_invite_code_request.state == 'pending':
                raise GetInviteCodeProcessed
            if get_invite_code_request.state == 'accepted':
                raise GetInviteCodeAccepted
            if get_invite_code_request.state == 'rejected':
                raise GetInviteCodeRejected

        get_invite_code_request = GetInviteCodeRequest(email=email, state='pending')

        # Temporary solution
        invite_code = await create_new_invite_code()
        get_invite_code_request.state = 'accepted'
        get_invite_code_request.code = invite_code
        await get_invite_code_request.commit()
        await spawn(self.request,
                    send_email_in_background(
                        GET_INVITE_CODE['mail']['text'].format(code=invite_code),
                        GET_INVITE_CODE['mail']['subject'],
                        SENDER_EMAIL,
                        email,
                        GET_INVITE_CODE['mail']['send_timeout']
                    ))

        raise Ok
