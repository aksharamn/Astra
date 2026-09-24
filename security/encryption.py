import base64
import os
import binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from .keys import master_key


def encrypt(value: str, key=None) -> str:
    nonce = os.urandom(12)
    token = nonce + AESGCM(key or master_key()).encrypt(nonce, value.encode(), None)
    return base64.urlsafe_b64encode(token).decode()


def decrypt(token: str, key=None) -> str:
    raw = base64.urlsafe_b64decode(token.encode())
    return AESGCM(key or master_key()).decrypt(raw[:12], raw[12:], None).decode()


def encrypt_payload(value: str, key=None) -> dict:
    nonce = os.urandom(12)
    sealed = AESGCM(key or master_key()).encrypt(nonce, value.encode(), None)
    return {"ciphertext": base64.urlsafe_b64encode(sealed[:-16]).decode(),
            "nonce": base64.urlsafe_b64encode(nonce).decode(),
            "tag": base64.urlsafe_b64encode(sealed[-16:]).decode()}


def decrypt_payload(payload: dict, key=None) -> str:
    nonce = base64.urlsafe_b64decode(payload["nonce"])
    sealed = base64.urlsafe_b64decode(payload["ciphertext"]) + base64.urlsafe_b64decode(payload["tag"])
    return AESGCM(key or master_key()).decrypt(nonce, sealed, None).decode()
