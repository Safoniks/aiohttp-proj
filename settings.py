import os
import sys

import logging
from logging.handlers import RotatingFileHandler
from logging.config import dictConfig


HOST = '0.0.0.0'
PORT = 8000

DEBUG = True

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = 'static'
UPLOAD_DIR = 'static/uploads'
DATA_DIR = 'data'
LOGS_DIR = 'logs'

if not os.path.exists(os.path.join(BASE_DIR, UPLOAD_DIR)):
    os.mkdir(os.path.join(BASE_DIR, UPLOAD_DIR))

STATIC_URL = '/static'
UPLOAD_URL = '/uploads'


def get_secret():
    path = os.path.join(BASE_DIR, DATA_DIR, 'secret.txt')
    if not os.path.exists(path):
        return '_){POJI:HUOP(@#$%F'
    with open(path) as f:
        secret = f.read()
        return secret

SECRET_KEY = get_secret()

ROUTES = {
    'URL_PREFIX': '/api/'
}

JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_DAYS = 30

DB_ALIAS = 'wmongo'
# DB_PORT = 27017
DB_PORT = 12021
DB_NAME = 'aiohttp'

TESTING = False
TESTING_DB_NAME = 'aiohttptest'

CONTACT_US_TARGET_EMAIL = 'test@gmail.com'
SENDER_EMAIL = "test@test.com"
SENDER_NAME = 'test'

LOG_FILE_BYTES = 10000
LOG_FILES_COUNT = 10

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'stdout': {
        'class': 'logging.StreamHandler',
        'stream': sys.stdout,
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['stdout']
    }
})


def configure_app_logs(log):
    path = os.path.join(BASE_DIR, LOGS_DIR)
    if not os.path.exists(path):
        os.mkdir(path)

    logs_file_name = os.path.join(BASE_DIR, LOGS_DIR, 'aiohttp.log')
    file_handler = RotatingFileHandler(logs_file_name, backupCount=LOG_FILES_COUNT,
                                       maxBytes=LOG_FILE_BYTES)
    log.addHandler(file_handler)
    return log

log = configure_app_logs(logging.getLogger('werkzeug'))


SCHEDULER_RUN_DATE_FORMAT = '%Y-%m-%d %H-%M-%S'
DATE_FORMAT = '%Y-%m-%d'
PAGE_SIZE_PAGINATION = 20

PASSWORD_LENGTH = 8
ALLOWED_MONTH_COUNT_TO_RESTORE = 3
INVITE_CODE_LENGTH = 4
GET_INVITE_CODE_REQUEST_TIMEOUT_IN_SECONDS = 300

RESTORE_PASSWORD = {
    'mail': {
        'text': 'Your new password - {password}',
        'subject': 'W:Here password restore'
    }
}
GET_INVITE_CODE = {
    'mail': {
        'text': 'Your invite code - {code}',
        'subject': 'W:Here get invite code',
        'send_timeout': 300
    }
}
