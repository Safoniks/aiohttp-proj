from umongo import Document, fields, validate
from models.main import instance

__all__ = (
    'LookingFor',
    'Recommendation',
)


@instance.register
class LookingFor(Document):
    title = fields.StrField(required=True)
    description = fields.StrField()
    skills = fields.ListField(fields.ReferenceField('Tag'))
    recommendations = fields.ListField(fields.ReferenceField('Recommendation'))
    date = fields.DateTimeField()
    only_for_my_contacts = fields.BoolField()


@instance.register
class Recommendation(Document):
    to_user = fields.ReferenceField('User', required=True)
    who_recommended = fields.ReferenceField('User', required=True)
    whom_recommended = fields.ReferenceField('User', required=True)
    rate = fields.ReferenceField('Rate', allow_none=True)
    date_recommended = fields.DateTimeField()
