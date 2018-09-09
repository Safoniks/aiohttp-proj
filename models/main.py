from motor import motor_asyncio as ma
from umongo import Instance

import settings
from utils import utils

host = utils.get_connection_string_for_alias(settings.DB_ALIAS)
db = utils.get_db_name()

print("URL:", host)
client = ma.AsyncIOMotorClient(host)
db = client[db]
instance = Instance(db)


INVITE_TYPE = [
    'personal',
    'group',
    'admin',
]
SOCIAL_LINK_TYPES = [
    'personal_url',
    'linkedin',
    'instagram',
    'twitter',
]
LANGUAGE_LEVELS = [
    'beginner',
    'intermediate',
    'upper_intermediate',
    'advanced',
    'fluent',
]
PREFERRED_WAYS_TO_MEET = [
    'breakfast',
    'after_work',
    'lunch',
    'call',
    'weekend',
]
TAG_TYPES = [
    'industry',
    'skill',
    'interest',
]
GET_INVITE_CODE_STATE = [
    'pending',
    'accepted',
    'rejected',
]
ADD_TAG_REQUEST_STATE = [
    'pending',
    'accepted',
    'rejected',
]
MEETING_TYPES = [
    'formal',
    'informal',
    'meet_with_third',
]
MEETING_STATES = [
    'pending',
    'accepted',
    'declined',
]
RESET_LINK_TYPE = [
    'restore_deleted',
    'reset_password',
]
USER_RELATIONSHIP_STATUS = [
    'pending',
    'accepted',
    'rejected',
    'blocked',
    'deleted',
]
CHAT_TYPE = [
    'dialogue',
    'group',
]
CHAT_MESSAGE_TYPE = [
    'text',
    'photo',
    'invite_to_meeting',
    'recommend_contact',
    'send_contact',
    'meeting_invite',
    'you_was_invited',
    'user_added_to_group',
    'user_removed_from_group',
    'trip_inform',
]
