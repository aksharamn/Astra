from datetime import datetime, timezone
from .db import db
from security.keys import secure_id
import secrets
import re


def now():
    return datetime.now(timezone.utc)


ASTRA_ALPHABET = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def generate_astra_id():
    return "".join(secrets.choice(ASTRA_ALPHABET) for _ in range(12))


ASTRA_ID_RE = re.compile(r"^[A-HJ-NP-Z2-9]{12}$")


def normalize_astra_id(value):
    compact = str(value or "").strip().upper()
    if compact.startswith("ASTRA-"):
        compact = compact[6:]
    compact = compact.replace("-", "")
    return compact if ASTRA_ID_RE.fullmatch(compact) else None


def format_astra_id(value):
    compact = normalize_astra_id(value)
    return f"ASTRA-{compact[:4]}-{compact[4:8]}-{compact[8:]}" if compact else None


class User(db.Model):
    id = db.Column(db.String(40), primary_key=True, default=lambda: secure_id("U"))
    astra_id = db.Column(db.String(12), unique=True, nullable=False, index=True,
                         default=generate_astra_id)
    username = db.Column(db.String(32), unique=True, nullable=False, index=True)
    email = db.Column(db.String(254), unique=True, index=True, nullable=True)
    pin_hash = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(280), default="")
    avatar = db.Column(db.String(255), default="")
    theme = db.Column(db.String(40), default="astra-dark")
    settings = db.Column(db.JSON, default=dict)
    session_version = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=now, nullable=False)


class ContactRequest(db.Model):
    id = db.Column(db.String(40), primary_key=True, default=lambda: secure_id("CR"))
    sender_id = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    recipient_id = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(16), default="pending", nullable=False)
    created_at = db.Column(db.DateTime, default=now, nullable=False)
    __table_args__ = (db.UniqueConstraint("sender_id", "recipient_id", name="uq_contact_pair"),)


class Message(db.Model):
    id = db.Column(db.String(40), primary_key=True, default=lambda: secure_id("M"))
    sender_id = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    recipient_id = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    ciphertext = db.Column(db.Text, nullable=False)
    nonce = db.Column(db.String(32), nullable=False, default="")
    tag = db.Column(db.String(32), nullable=False, default="")
    delivery_status = db.Column(db.String(16), default="delivered", nullable=False)
    read_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=now, nullable=False)


class RecoveryChallenge(db.Model):
    id = db.Column(db.String(40), primary_key=True, default=lambda: secure_id("RC"))
    user_id = db.Column(db.String(40), db.ForeignKey("user.id"), nullable=False)
    challenge_hash = db.Column(db.String(255), nullable=False)
    token_hash = db.Column(db.String(255))
    expires_at = db.Column(db.DateTime, nullable=False)
    used = db.Column(db.Boolean, default=False, nullable=False)
