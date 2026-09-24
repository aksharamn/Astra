from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError

_hasher = PasswordHasher()


def hash_secret(value: str) -> str:
    if not isinstance(value, str) or not value:
        raise ValueError("secret is required")
    return _hasher.hash(value)


def verify_secret(encoded: str, value: str) -> bool:
    try:
        return bool(encoded and value and _hasher.verify(encoded, value))
    except (VerifyMismatchError, VerificationError, TypeError):
        return False
