from umongo import Document, fields, validate
from models.main import instance, CHAT_TYPE, CHAT_MESSAGE_TYPE

__all__ = (
    'Chat',
    'ChatMember',
    'ChatMessage',
)


@instance.register
class Chat(Document):
    owner = fields.ReferenceField('User', required=True)
    members = fields.ListField(fields.ReferenceField('ChatMember'))
    name = fields.StrField()
    description = fields.StrField()
    type = fields.StrField(validate=validate.OneOf(CHAT_TYPE), required=True)
    last_message = fields.ReferenceField('ChatMessage', allow_none=True)
    created = fields.DateTimeField()


@instance.register
class ChatMember(Document):
    user = fields.ReferenceField('User', required=True)
    chat = fields.ReferenceField('Chat', required=True)
    is_notifications_enabled = fields.BoolField()
    is_active = fields.BoolField()
    last_visited = fields.DateTimeField()
    # status = fields.StrField()
    # unread_messages_count = fields.IntField(validate=validate.Range(min=0))


@instance.register
class ChatMessage(Document):
    sender = fields.ReferenceField('ChatMember', required=True)
    type = fields.StrField(validate=validate.OneOf(CHAT_MESSAGE_TYPE))
    body = fields.StrField()
    date_sended = fields.DateTimeField()
