import re
import secrets
import logging
from datetime import datetime, timedelta, timezone
from flask import Blueprint, jsonify, request
from database.db import db
from database.models import User, RecoveryChallenge, format_astra_id, normalize_astra_id
from security.hashing import hash_secret, verify_secret
from security.sessions import login_user, logout_user, require_auth, current_user


def user_json(user):
    return {"id": user.id, "astra_id": user.astra_id,
            "astra_id_display": format_astra_id(user.astra_id),
            "username": user.username, "display_name": user.display_name,
            "avatar": user.avatar, "theme": user.theme, "settings": user.settings or {}}

bp = Blueprint("auth", __name__, url_prefix="/api/auth")
_attempts = {}
security_log = logging.getLogger("astra.security")


def _limited(ip):
    now = datetime.now(timezone.utc).timestamp()
    values = [t for t in _attempts.get(ip, []) if now - t < 60]
    values.append(now)
    _attempts[ip] = values
    return len(values) > 12


def _record_or_reject(ip, bucket, limit=12):
    key = f"{bucket}:{ip}"
    return _limited(key)


def _valid_pin(pin):
    return isinstance(pin, str) and bool(re.fullmatch(r"\d{6,12}", pin))


def _normalize_email(value):
    email = str(value or "").strip().lower()
    return email if re.fullmatch(r"[^@\s]{1,64}@[^@\s]{1,64}\.[^@\s]{2,63}", email) else None


@bp.post("/register")
def register():
    if _record_or_reject(request.remote_addr or "unknown", "register"):
        return jsonify(error="too many attempts"), 429
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip().lower()
    email = _normalize_email(data.get("email"))
    pin = data.get("pin")
    display = str(data.get("display_name") or username).strip()
    if not re.fullmatch(r"[a-z0-9_]{3,32}", username) or not email or not _valid_pin(pin) or not (1 <= len(display) <= 80):
        return jsonify(error="email, username, PIN, or display name is invalid"), 400
    if username and User.query.filter_by(username=username).first():
        return jsonify(error="username already exists"), 409
    if User.query.filter_by(email=email).first():
        return jsonify(error="email already exists"), 409
    astra_id = None
    while astra_id is None or User.query.filter_by(astra_id=astra_id).first():
        from database.models import generate_astra_id
        astra_id = generate_astra_id()
    user = User(astra_id=astra_id, username=username, email=email, pin_hash=hash_secret(pin), display_name=display)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify(user=user_json(user), astra_id=user.astra_id), 201


@bp.post("/login")
def login():
    if _limited(request.remote_addr or "unknown"):
        return jsonify(error="too many attempts"), 429
    data = request.get_json(silent=True) or {}
    identifier = str(data.get("identifier") or data.get("username") or data.get("astra_id") or "").strip()
    astra_id = normalize_astra_id(identifier)
    username = identifier.lower()
    email = _normalize_email(identifier)
    if astra_id:
        user = User.query.filter_by(astra_id=astra_id).first()
    elif email:
        user = User.query.filter_by(email=email).first()
    else:
        user = User.query.filter_by(username=username).first()
    if not user or not verify_secret(user.pin_hash, data.get("pin", "")):
        security_log.warning("authentication failure from %s", request.remote_addr or "unknown")
        return jsonify(error="invalid credentials"), 401
    login_user(user)
    return jsonify(user=user_json(user))


@bp.post("/logout")
def logout():
    logout_user()
    return jsonify(ok=True)


@bp.get("/me")
@require_auth
def me():
    u = current_user()
    result = user_json(u); result["bio"] = u.bio
    return jsonify(user=result)


@bp.post("/recovery/request")
def recovery_request():
    if _record_or_reject(request.remote_addr or "unknown", "recovery"):
        return jsonify(error="too many attempts"), 429
    data = request.get_json(silent=True) or {}
    user = User.query.filter_by(astra_id=normalize_astra_id(data.get("astra_id"))).first()
    # Do not disclose whether an account exists.
    if not user:
        return jsonify(ok=True)
    challenge = secrets.token_urlsafe(24)
    row = RecoveryChallenge(user_id=user.id, challenge_hash=hash_secret(challenge),
                            expires_at=datetime.now(timezone.utc) + timedelta(minutes=10))
    db.session.add(row)
    db.session.commit()
    return jsonify(ok=True, challenge=challenge, challenge_id=row.id)


@bp.post("/recover")
def recover_alias():
    return recovery_request()


@bp.post("/recovery/reset")
def recovery_reset():
    data = request.get_json(silent=True) or {}
    challenge = RecoveryChallenge.query.get(data.get("challenge_id")) if data.get("challenge_id") else None
    if not challenge or challenge.used or challenge.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return jsonify(error="invalid or expired recovery challenge"), 400
    supplied = data.get("token") or data.get("challenge")
    valid = verify_secret(challenge.token_hash, supplied) if challenge.token_hash else verify_secret(challenge.challenge_hash, supplied)
    if not valid or not _valid_pin(data.get("pin")):
        return jsonify(error="invalid recovery data"), 400
    user = User.query.get(challenge.user_id)
    user.pin_hash = hash_secret(data["pin"])
    user.session_version += 1
    challenge.used = True
    db.session.commit()
    return jsonify(ok=True)


@bp.post("/recovery/verify")
def recovery_verify():
    """Exchange the one-time challenge for a short-lived reset token."""
    data = request.get_json(silent=True) or {}
    challenge = RecoveryChallenge.query.get(data.get("challenge_id")) if data.get("challenge_id") else None
    if not challenge or challenge.used or challenge.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        return jsonify(error="invalid or expired recovery challenge"), 400
    if not verify_secret(challenge.challenge_hash, data.get("challenge", "")):
        return jsonify(error="invalid recovery challenge"), 400
    token = secrets.token_urlsafe(32)
    challenge.token_hash = hash_secret(token)
    db.session.commit()
    return jsonify(token=token, challenge_id=challenge.id)
