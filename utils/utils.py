MEETING_INVITE_NOTIFICATION = 0
MEETING_ACCEPT_NOTIFICATION = 1
CONTACT_EXCHANGE_NOTIFICATION = 2
CONTACT_EXCHANGE_ACCEPT_NOTIFICATION = 3
TRIP_COMING_SOON_NOTIFICATION = 4
MEETING_REMINDER_NOTIFICATION = 5
NEW_TRIP_FOR_CONTACTS_NOTIFICATION = 6
MEETING_CANCELED_NOTIFICATION = 7
SUGGEST_RATE_USER_NOTIFICATION = 8
RECOMMENDATION_NOTIFICATION = 9

NOTIFICATION_PREVIEWS = {
    MEETING_INVITE_NOTIFICATION: "{sender} is asking you for a meeting",
    MEETING_ACCEPT_NOTIFICATION: "{sender} {accept} your offer for a meeting",
    CONTACT_EXCHANGE_NOTIFICATION: "{sender} wants to exchange contacts with you",
    CONTACT_EXCHANGE_ACCEPT_NOTIFICATION: "{sender} {accept} your offer to exchange contacts",
    TRIP_COMING_SOON_NOTIFICATION: "{sender} has trip to your city",
    MEETING_REMINDER_NOTIFICATION: "You have meeting soon with {sender}",
    NEW_TRIP_FOR_CONTACTS_NOTIFICATION: "{sender} has a trip to your city soon",
    MEETING_CANCELED_NOTIFICATION: "{sender} canceled meeting",
    SUGGEST_RATE_USER_NOTIFICATION: "Please, rate {sender}",
    RECOMMENDATION_NOTIFICATION: "{sender} recommended some users for you"
}

import os
import settings
import hashlib
import random
import string
import uuid
from smtplib import SMTP_SSL, SMTPException
from socket import gaierror
from email.mime.text import MIMEText

from exceptions import EmailSendingInternal


def get_hash(str_obj: str) -> str:
    m = hashlib.sha256()
    m.update(str_obj.encode('utf-8'))
    return m.digest().hex()


def get_db_name():
    return settings.TESTING_DB_NAME if settings.TESTING else settings.DB_NAME


def get_default_connection_string():
    return 'mongodb://localhost:{0}/{1}'.format(settings.DB_PORT, get_db_name())


def get_connection_string_for_alias(alias):
    envs = os.environ
    for key in envs:
        if '_'.join((alias.upper(), 'PORT')) in key and len(key.split('_')) == 4:
            address = 'mongodb:' + envs[key].split(':', 1)[-1]
            return address + '/' + get_db_name()
    return get_default_connection_string()


def generate_code(code_length):
    result = [random.choice(string.ascii_letters + string.digits) for _ in range(code_length)]
    return ''.join(result)


def generate_password():
    return str(uuid.uuid4())[:settings.PASSWORD_LENGTH]


def send_email(message, subject, from_email, to_email):
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        s = SMTP_SSL(settings.MAIL_SERVER, settings.MAIL_PORT)
        s.login(settings.MAIL_USERNAME, settings.MAIL_PASSWORD)
        s.send_message(msg)
        s.quit()
    except (SMTPException, gaierror) as ex:
        settings.log.debug('Failed sending mail to {}'.format(to_email))
        raise EmailSendingInternal(detail=ex.strerror)


def get_page(query):
    page = query.get('page', None)
    pagesize = query.get('pagesize', None)

    if page is not None and page.isnumeric():
        page = int(page) if int(page) > 0 else None
    else:
        page = None
    if pagesize is not None and pagesize.isnumeric():
        pagesize = int(pagesize) if int(pagesize) > 0 else None
    else:
        pagesize = None

    return page, pagesize


def get_objects_with_pagination(objects, page=None, pagesize=None):
    if page is None and pagesize is None:
        result = objects
    else:
        pagesize = pagesize if pagesize is not None else settings.PAGE_SIZE_PAGINATION
        page = page if page is not None else 1
        result = objects.skip(pagesize*(page-1)).limit(pagesize)
    return result
