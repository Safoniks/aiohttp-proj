from aiohttp import web
from aiohttp_utils import Response

from models.main import TAG_TYPES
from models.tag import TagSynonym
from api.middleware_view import with_pagination

from exceptions import (
    NoGetParameters,
)

from utils.utils import get_objects_with_pagination


class GetTags(web.View):

    @with_pagination()
    async def get(self, **kw):
        query = dict(self.request.query)
        pagination = self.request.pagination
        search = query.get('contains', None)
        tag_type = query.get('type', None)
        parent = query.get('parent', None)

        search_filter = {}
        if search is not None and tag_type in TAG_TYPES:
            search_filter['name'] = {'$regex': '.*{0}.*'.format(search), '$options': 'i'}
            search_filter['type'] = tag_type
            if parent is not None:
                search_filter['parent'] = parent
        else:
            raise NoGetParameters

        tags = TagSynonym.find(search_filter)
        tags = get_objects_with_pagination(tags, **pagination)
        tags = await tags.to_list(None)
        tags = [tag.parent_synonym for tag in tags]
        return Response(tags)
