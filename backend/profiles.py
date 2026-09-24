from flask import Blueprint, jsonify, request, g
from database.db import db
from security.sessions import require_auth
from database.models import User, format_astra_id, normalize_astra_id

bp = Blueprint("profiles", __name__, url_prefix="/api/profile")


@bp.get("/<user_id>")
@require_auth
def get_profile(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(id=user.id, astra_id=user.astra_id,
                   astra_id_display=format_astra_id(user.astra_id),
                   username=user.username, display_name=user.display_name, bio=user.bio,
                   avatar=user.avatar, theme=user.theme, settings=user.settings or {})


@bp.patch("")
@require_auth
def update_profile():
    data = request.get_json(silent=True) or {}
    if "display_name" in data:
        name = str(data["display_name"]).strip()
        if not 1 <= len(name) <= 80:
            return jsonify(error="invalid display name"), 400
        g.user.display_name = name
    if "bio" in data:
        bio = str(data["bio"]).strip()
        if len(bio) > 280:
            return jsonify(error="bio is too long"), 400
        g.user.bio = bio
    for field in ("avatar", "theme", "settings"):
        if field in data:
            if field == "settings" and not isinstance(data[field], dict):
                return jsonify(error="settings must be an object"), 400
            setattr(g.user, field, data[field])
    db.session.commit()
    return jsonify(ok=True)


@bp.get("/by-astra-id/<astra_id>")
@require_auth
def get_profile_by_astra_id(astra_id):
    user = User.query.filter_by(astra_id=normalize_astra_id(astra_id)).first()
    if not user or user.id == g.user.id:
        return jsonify(error="ASTRA ID not found"), 404
    return jsonify(id=user.id, astra_id=user.astra_id,
                   astra_id_display=format_astra_id(user.astra_id),
                   username=user.username, display_name=user.display_name,
                   bio=user.bio, avatar=user.avatar)
