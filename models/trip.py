from umongo import Document, fields, validate
from models.main import instance
from models.embedded_models import Location

__all__ = (
    'Trip',
)


@instance.register
class Trip(Document):
    user = fields.ReferenceField('User', required=True)
    from_location = fields.EmbeddedField(Location, required=True)
    to_location = fields.EmbeddedField(Location, required=True)
    start_date = fields.DateTimeField(required=True)
    end_date = fields.DateTimeField(required=True)
    purpose = fields.StrField()
    tags_to_discuss = fields.ListField(fields.ReferenceField('Tag'))
    notify_users = fields.BoolField(missing=True)
