from datetime import datetime

from umongo import Document, fields, validate
from models.main import instance, MEETING_TYPES, MEETING_STATES

__all__ = (
    'MeetingMember',
    'Meeting',
)


@instance.register
class MeetingMember(Document):
    user = fields.ReferenceField('User', required=True)
    meeting = fields.ReferenceField('Meeting', required=True)
    rate = fields.ReferenceField('Rate', allow_none=True)


@instance.register
class Meeting(Document):
    owner = fields.ReferenceField('User', required=True)
    members = fields.ListField(fields.ReferenceField('MeetingMember'))
    meeting_type = fields.StrField(validate=validate.OneOf(MEETING_TYPES), required=True)
    state = fields.StrField(validate=validate.OneOf(MEETING_STATES))
    description = fields.StrField()

    place_address = fields.StrField()
    latitude = fields.FloatField()
    longitude = fields.FloatField()
    google_place_id = fields.IntField()
    google_place_city_id = fields.IntField()

    date_created = fields.DateTimeField(missing=datetime.now())
    date_resolved = fields.DateTimeField(required=True)
