from bson import ObjectId

from models.user import User
from models.other import InviteGroup, GetInviteCodeRequest

from utils.utils import generate_code
from settings import INVITE_CODE_LENGTH

__all__ = (
    'is_valid_invited_by',
    'exist_invite_code',
    'create_new_invite_code',
)


async def is_valid_invited_by(id):
    if not await InviteGroup.find_one({'_id': ObjectId(id)}) and \
            not await User.find_one({'_id': ObjectId(id)}) and \
            not await GetInviteCodeRequest.find_one({'_id': ObjectId(id)}):
        return False
    return True


async def exist_invite_code(code):
    if not await InviteGroup.find_one({'code': code}) and \
            not await User.find_one({'personal_invite_code': code}) and \
            not await GetInviteCodeRequest.find_one({'code': code, 'state': 'accepted'}):
        return False
    return True


async def create_new_invite_code():
    while True:
        invite_code = generate_code(INVITE_CODE_LENGTH)
        if not await exist_invite_code(invite_code):
            break
    return invite_code
