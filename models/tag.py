from datetime import datetime

from pymongo import IndexModel, ASCENDING
from umongo import Document, fields, validate, ValidationError
from models.main import instance, TAG_TYPES, ADD_TAG_REQUEST_STATE

__all__ = (
    'Tag',
    'TagSynonym',
    'AddTagRequest',
)


@instance.register
class Tag(Document):
    name = fields.StrField(required=True)
    type = fields.StrField(validate=validate.OneOf(TAG_TYPES), required=True)
    parent = fields.StrField(allow_none=True)

    class Meta:
        indexes = [IndexModel([('name', ASCENDING), ('type', ASCENDING)], unique=True), '$name']

    @classmethod
    async def validate_tags(cls, tag_names):
        tags = []
        for tag_name in tag_names:
            tag = await cls.validate_tag(tag_name)
            tags.append(tag)
        return tags

    @classmethod
    async def validate_tag(cls, tag_name):
        tag = await cls.find_one({'name': tag_name})
        if tag is not None:
            return tag
        else:
            raise ValidationError('No tag with this name({}).'.format(tag_name))


@instance.register
class TagSynonym(Document):
    name = fields.StrField(required=True)
    type = fields.StrField(validate=validate.OneOf(TAG_TYPES), required=True)
    parent = fields.StrField(allow_none=True)
    parent_synonym = fields.StrField(required=True)

    class Meta:
        indexes = [IndexModel(
            [('name', ASCENDING), ('type', ASCENDING), ('parent_synonym', ASCENDING)],
            unique=True
        ), '$name']


@instance.register
class AddTagRequest(Document):
    user = fields.ReferenceField('User', required=True)
    tag_name = fields.StrField(required=True)
    type = fields.StrField(validate=validate.OneOf(TAG_TYPES))
    state = fields.StrField(validate=validate.OneOf(ADD_TAG_REQUEST_STATE))
    date = fields.DateTimeField(missing=datetime.now())

    @property
    def repeats_count(self):
        return 0
