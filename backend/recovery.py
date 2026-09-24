"""Recovery policy helpers. Recovery endpoints are registered by backend.auth."""
from datetime import datetime, timezone


def is_expired(value):
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value <= datetime.now(timezone.utc)
