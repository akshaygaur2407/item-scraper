# backend/app/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# one shared limiter instance, with your defaults
limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])
