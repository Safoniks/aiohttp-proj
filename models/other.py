from datetime import datetime

from umongo import Document, fields, validate
from models.main import instance, RESET_LINK_TYPE, GET_INVITE_CODE_STATE

from settings import INVITE_CODE_LENGTH

__all__ = (
    'Rate',
    'ResetLink',
    'InviteGroup',
    'GetInviteCodeRequest',
)


@instance.register
class Rate(Document):
    from_user = fields.ReferenceField('User', required=True)
    to_user = fields.ReferenceField('User', required=True)
    rate = fields.IntField(required=True, validate=validate.Range(min=1, max=5))
    description = fields.StrField()
    date = fields.DateTimeField()


@instance.register
class ResetLink(Document):
    user = fields.ReferenceField('User', required=True)
    code = fields.StrField(required=True)
    type = fields.StrField(required=True, validate=validate.OneOf(RESET_LINK_TYPE))
    is_used = fields.BoolField(missing=False)
    date_created = fields.DateTimeField(missing=datetime.now())
    date_valid = fields.DateTimeField(allow_none=True)


@instance.register
class InviteGroup(Document):
    code = fields.StrField(unique=True, required=True, validate=validate.Length(equal=INVITE_CODE_LENGTH))
    limit = fields.IntField(required=True, validate=validate.Range(min=1))
    available_uses = fields.IntField(required=True, validate=validate.Range(min=0))
    # expiration_date = fields.DateTimeField()

    async def create_new_code(self, limit, code=None):
        from models.utils import create_new_invite_code

        self.code = code if code is not None else await create_new_invite_code()
        self.limit = limit
        self.available_uses = limit
        await self.commit()
        return self


@instance.register
class GetInviteCodeRequest(Document):
    email = fields.EmailField(unique=True, required=True)
    code = fields.StrField(unique=True, required=False, validate=validate.Length(equal=INVITE_CODE_LENGTH))
    state = fields.StrField(required=True, validate=validate.OneOf(GET_INVITE_CODE_STATE))
    created = fields.DateTimeField(missing=datetime.now())
