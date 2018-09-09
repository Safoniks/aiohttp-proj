from umongo import EmbeddedDocument, fields, validate, ValidationError
from models.main import instance, SOCIAL_LINK_TYPES, LANGUAGE_LEVELS

__all__ = (
    'Bubble',
    'SocialLink',
    'Language',
    'Location',
    'Industry',
)


@instance.register
class Bubble(EmbeddedDocument):
    position_x = fields.FloatField()
    position_y = fields.FloatField()
    tags = fields.ListField(fields.ReferenceField('Tag'))


@instance.register
class SocialLink(EmbeddedDocument):
    value = fields.UrlField(required=True)
    type = fields.StrField(validate=validate.OneOf(SOCIAL_LINK_TYPES), required=True)


@instance.register
class Language(EmbeddedDocument):
    name = fields.StrField(required=True)
    level = fields.StrField(validate=validate.OneOf(LANGUAGE_LEVELS), required=True)


@instance.register
class Location(EmbeddedDocument):
    google_place_city_id = fields.IntField()
    city_name = fields.StrField()
    country_name = fields.StrField()


@instance.register
class Industry(EmbeddedDocument):
    industry = fields.ReferenceField('Tag', required=True)
    experience = fields.IntField(required=True, validate=validate.Range(min=0, max=100))
