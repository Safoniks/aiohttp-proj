import asyncio

from utils.utils import send_email

async def send_email_in_background(message, subject, from_email, to_email, timeout=0):
    await asyncio.sleep(timeout)
    send_email(message, subject, from_email, to_email)
