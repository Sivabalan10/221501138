import random
import string
import validators
from datetime import datetime, timedelta

def generate_shortcode(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def shorten_url(long_url, validity=None, shortcode=None):
    if not validators.url(long_url):
        raise ValueError("Invalid URL format")
    if not validity:
        validity = 30  # minutes
    expiry = datetime.utcnow() + timedelta(minutes=int(validity))
    if not shortcode:
        shortcode = generate_shortcode()
    return shortcode, expiry.isoformat()