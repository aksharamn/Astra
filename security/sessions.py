from functools import wraps
from flask import g, jsonify, session
from database.models import User


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    user = User.query.filter_by(id=user_id).first()
    if not user or session.get("session_version") != user.session_version:
        session.clear()
        return None
    return user


def login_user(user):
    session.clear()
    session["user_id"] = user.id
    session["session_version"] = user.session_version
    g.user = user


def logout_user():
    session.clear()
    g.pop("user", None)


def require_auth(fn):
    @wraps(fn)
    def wrapped(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify(error="authentication required"), 401
        g.user = user
        return fn(*args, **kwargs)
    return wrapped
