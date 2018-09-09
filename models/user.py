from datetime import datetime
from werkzeug.security import safe_str_cmp

from umongo import Document, fields, validate, ValidationError
from models.main import instance, PREFERRED_WAYS_TO_MEET, USER_RELATIONSHIP_STATUS, INVITE_TYPE
from models.tag import Tag
from models.looking_for import LookingFor
from models.embedded_models import (
    Language,
    Location,
    SocialLink,
    Industry,
    Bubble,
)

from utils.utils import (get_hash, )
from settings import INVITE_CODE_LENGTH, DATE_FORMAT

__all__ = (
    'UserRelationship',
    'UserReport',
    'SystemUser',
    'User',
)


@instance.register
class UserRelationship(Document):
    from_user = fields.ReferenceField('User', required=True)
    to_user = fields.ReferenceField('User', required=True)
    status = fields.StrField(validate=validate.OneOf(USER_RELATIONSHIP_STATUS))
    date = fields.DateTimeField()

    @classmethod
    async def get_users_relationship(cls, user1_id, user2_id):
        relationship = await cls.find_one({'$or': [
            {'from_user': user1_id, 'to_user': user2_id},
            {'from_user': user2_id, 'to_user': user1_id},
        ]})
        return relationship

    @classmethod
    async def create_or_update_relationship(cls, from_user_id, to_user_id, status):
        relationship = await cls.get_users_relationship(from_user_id, to_user_id)
        if relationship:
            relationship.from_user = from_user_id
            relationship.to_user = to_user_id
            relationship.status = status
        else:
            relationship = cls(
                from_user=from_user_id,
                to_user=to_user_id,
                status=status,
                data=datetime.utcnow(),
            )
        await relationship.commit()


@instance.register
class UserReport(Document):
    reporting_user = fields.ReferenceField('User', required=True)
    bad_user = fields.ReferenceField('User', required=True)
    description = fields.StrField()
    date = fields.DateTimeField(missing=datetime.now())


@instance.register
class UsersMixin(Document):
    password = fields.StrField(required=True, validate=validate.Length(min=5))

    class Meta:
        allow_inheritance = True
        abstract = True

    def set_password(self, password: str):
        self.password = get_hash(password)

    def check_password(self, password: str) -> bool:
        return safe_str_cmp(self.password, get_hash(password))


@instance.register
class SystemUser(UsersMixin):
    email = fields.StrField(unique=True, required=True)
    active = fields.BoolField()


@instance.register
class User(UsersMixin):
    def _validate_industries(field, value):
        for industry in value:
            yield from industry.industry.fetch(no_data=True)

    def _validate_invited_by(field, value):
        from models.utils import is_valid_invited_by
        if not (yield from is_valid_invited_by(value)):
            raise ValidationError('There is no such user or group code.')

    fullname = fields.StrField(required=True)
    email = fields.EmailField(unique=True, required=True)
    nickname = fields.StrField(unique=True, required=True, validate=validate.Regexp(r'[\w\d]+'))
    birthday = fields.DateTimeField(required=True, format=DATE_FORMAT)
    phone_numbers = fields.ListField(fields.StrField(validate=validate.Regexp(r'[+][\w\d]+')), required=True)
    photo = fields.StrField(required=True)
    bio = fields.StrField(required=False, validate=validate.Length(max=320))
    organizations = fields.StrField(required=False, validate=validate.Length(max=320))
    education = fields.StrField(required=False, validate=validate.Length(max=320))
    personal_invite_code = fields.StrField(unique=True, required=True, validate=validate.Length(equal=INVITE_CODE_LENGTH))

    social_links = fields.ListField(fields.EmbeddedField(SocialLink))
    current_location = fields.EmbeddedField(Location)
    preferred_ways_to_meet = fields.ListField(fields.StrField(validate=validate.OneOf(PREFERRED_WAYS_TO_MEET)), unique=True)

    join_date = fields.DateTimeField(missing=datetime.utcnow())
    is_active = fields.BoolField(missing=False)
    is_deleted = fields.BoolField()
    date_deleted = fields.DateTimeField()
    is_notifications_enabled = fields.BoolField(missing=True)

    skills = fields.ListField(fields.ReferenceField(Tag), required=True)
    interests = fields.ListField(fields.ReferenceField(Tag))
    industries = fields.ListField(fields.EmbeddedField(Industry), required=True, io_validate=_validate_industries)
    languages = fields.ListField(fields.EmbeddedField(Language))

    looking_for = fields.ListField(fields.ReferenceField(LookingFor))
    bubbles = fields.ListField(fields.EmbeddedField(Bubble))

    invited_type = fields.StrField(required=True, validate=validate.OneOf(INVITE_TYPE))
    invited_by = fields.StrField(required=True, io_validate=_validate_invited_by)
