import json
import jwt
from bson import ObjectId
from aiohttp.web import middleware, Response
from aiohttp.web_exceptions import HTTPException

from marshmallow.exceptions import ValidationError
from exceptions import DomainException, InvalidJWTAuthorization, ExpiredToken, InvalidJWTToken
from settings import JWT_SECRET, JWT_ALGORITHM
from models.user import User


@middleware
async def error_middleware(request, handler):
    try:
        response = await handler(request)
        return response
    except (ValidationError, HTTPException) as ex:
        status = getattr(ex, 'status_code', 400)
        message = {
            'code': ex.__class__.__name__,
            'detail': getattr(ex, 'messages', '') or getattr(ex, 'text', ''),
        }
        text = json.dumps(message)
        return Response(content_type='application/json', text=text, status=status)
    except Exception as ex:
        try:
            status = ex.status_code
            text = json.dumps(ex.to_dict())
            return Response(content_type='application/json', text=text, status=status)
        except AttributeError:
            exception = DomainException()
            status = exception.status_code
            text = json.dumps(exception.to_dict())
            return Response(content_type='application/json', text=text, status=status)


@middleware
async def auth_middleware(request, handler):
    request.user = None
    authorization = request.headers.get('authorization', None)

    if authorization:
        try:
            key_authorization, value_authorization = authorization.split(' ')
            assert key_authorization == 'JWT'
            jwt_token = value_authorization
        except (ValueError, AssertionError):
            raise InvalidJWTAuthorization

        try:
            payload = jwt.decode(jwt_token, JWT_SECRET,
                                 algorithms=[JWT_ALGORITHM])
        except jwt.DecodeError:
            raise InvalidJWTToken
        except jwt.ExpiredSignatureError:
            raise ExpiredToken

        user = await User.find_one({'id': ObjectId(payload['user_id'])})
        if not user:
            raise InvalidJWTToken
        request.user = user
    return await handler(request)
