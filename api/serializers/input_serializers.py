import uuid
import os
from werkzeug.utils import secure_filename
from bson import ObjectId

from aiohttp.hdrs import CONTENT_TYPE
from umongo import post_load, fields, validate, ValidationError
from marshmallow import fields as marshmallow_fields, Schema

from models.user import User
from models.tag import Tag
from models.embedded_models import Industry
from exceptions import InvalidInputData

from models.utils import create_new_invite_code
from settings import BASE_DIR, UPLOAD_DIR, INVITE_CODE_LENGTH, DATE_FORMAT

__all__ = (
    'IndustryTagSchema',
    'InviteCodeSchema',
    'RegisterUserSchema',
    'register_user',
)


UNKNOWN_FIELD_ERROR_MESSAGE = 'Unknown field.'
MISSING_REQUIRED_FIELD_ERROR_MESSAGE = 'Missing data for required field.'

IndustrySchema = Industry.schema.as_marshmallow_schema()
UserSchema = User.schema.as_marshmallow_schema()


class IndustryTagSchema(IndustrySchema):
    industry = fields.StrField(required=True)


class InviteCodeSchema(Schema):
    invite_code = fields.StrField(required=True, validate=validate.Length(equal=INVITE_CODE_LENGTH))


class RegisterUserSchema(UserSchema):
    phone = fields.StrField(required=True, validate=validate.Regexp(r'[+][\w\d]+'))
    industry = marshmallow_fields.Nested(IndustryTagSchema, required=True)
    skills = fields.ListField(fields.StrField(), required=True, validate=validate.Length(min=1, max=10))
    interests = fields.ListField(fields.StrField(), validate=validate.Length(min=1, max=10))

    class Meta:
        fields = (
            'email',
            'password',
            'fullname',
            'nickname',
            'birthday',
            'phone',
            'current_location',
            'invited_type',
            'invited_by',
            'skills',
            'interests',
            'industry',
        )
        dateformat = DATE_FORMAT

    @post_load
    def make_user(self, data):
        data['phone_numbers'] = [data.pop('phone')]
        industry = data.pop('industry')
        skills = data.pop('skills')
        interests = data.pop('interests')
        user = User(**data)
        user.set_password(data['password'])
        return {
            'user': user,
            'industry': industry,
            'skills': skills,
            'interests': interests,
        }


async def register_user(form_data):
    REQUIRED_JSON_FIELD = 'json'
    REQUIRED_PHOTO_FIELD = 'photo'
    metadata = {}
    photo = {}
    _invalid_fields = {}

    while True:
        part = await form_data.next()
        if part is None:
            break

        if part.headers.get(CONTENT_TYPE, '') == 'application/json' and \
                        part.name == REQUIRED_JSON_FIELD and not metadata:
            metadata = await part.json()
            continue

        if 'image/' in part.headers.get(CONTENT_TYPE, '') and \
                        part.name == REQUIRED_PHOTO_FIELD and part.filename and not photo:
            photo['filename'] = part.filename
            photo['filedata'] = []
            while True:
                chunk = await part.read_chunk()  # 8192 bytes by default.
                if not chunk:
                    break
                photo['filedata'].append(chunk)
            continue

        _invalid_fields[part.name] = UNKNOWN_FIELD_ERROR_MESSAGE

    if not metadata:
        _invalid_fields.update({REQUIRED_JSON_FIELD: MISSING_REQUIRED_FIELD_ERROR_MESSAGE})

    if not photo:
        _invalid_fields.update({REQUIRED_PHOTO_FIELD: MISSING_REQUIRED_FIELD_ERROR_MESSAGE})

    if _invalid_fields:
        raise InvalidInputData(detail=_invalid_fields)

    data, _ = RegisterUserSchema(strict=True).load(metadata)
    user = data['user']
    industry = data['industry']

    industry_tag = await Tag.validate_tag(industry['industry'])
    industry['industry'] = industry_tag.pk
    skills = await Tag.validate_tags(data['skills'])
    interests = await Tag.validate_tags(data['interests'])
    user.industries = [industry]
    user.skills = [skill.pk for skill in skills]
    user.interests = [interest.pk for interest in interests]

    user.personal_invite_code = await create_new_invite_code()

    photo_name = str(uuid.uuid4()) + '.' + secure_filename(photo['filename']).rsplit('.', 1)[-1]
    photo_path = os.path.join(BASE_DIR, UPLOAD_DIR, photo_name)
    with open(photo_path, 'wb') as f:
        for chunk in photo['filedata']:
            f.write(chunk)

    user.photo = photo_name
    try:
        await user.commit()
    except ValidationError as ex:
        os.remove(photo_path)
        raise ex

    return user
