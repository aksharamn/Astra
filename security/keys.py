import base64
import hashlib
import os
import secrets


_process_master_key = secrets.token_bytes(32)


def secure_id(prefix="ASTRA", length=16):
    return f"{prefix}-{secrets.token_urlsafe(length)[:length].upper()}"


def master_key(config=None):
    raw = (config or {}).get("ASTRA_MASTER_KEY") if config else None
    raw = raw or os.getenv("ASTRA_MASTER_KEY")
    if raw:
        try:
            key = base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4))
            if len(key) == 32:
                return key
        except (ValueError, TypeError):
            pass
        return hashlib.sha256(raw.encode()).digest()
    # Development fallback is process-stable but never predictable or shared.
    return _process_master_key
