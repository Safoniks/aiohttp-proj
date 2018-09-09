from functools import wraps
from exceptions import NotAuthorized, AlreadyAuthenticated
from utils.utils import get_page


def jwt_required():
    def wrapper(func):
        @wraps(func)
        async def decorator(handle, *args, **kwargs):
            request = handle.request
            if not request.user:
                raise NotAuthorized
            return await func(handle, *args, **kwargs)
        return decorator
    return wrapper


def not_authenticated():
    def wrapper(func):
        @wraps(func)
        async def decorator(handle, *args, **kwargs):
            request = handle.request
            if request.user:
                raise AlreadyAuthenticated
            return await func(handle, *args, **kwargs)
        return decorator
    return wrapper


def with_pagination():
    def wrapper(func):
        @wraps(func)
        async def decorator(handle, *args, **kwargs):
            request = handle.request
            query = dict(request.query)
            page, pagesize = get_page(query)
            request.pagination = {
                'page': page,
                'pagesize': pagesize,
            }
            return await func(handle, *args, **kwargs)
        return decorator
    return wrapper
