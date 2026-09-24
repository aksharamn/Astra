from flask import Blueprint, jsonify, request, g
from database.db import db
from database.models import User, ContactRequest, format_astra_id, normalize_astra_id
from security.sessions import require_auth

bp = Blueprint("contacts", __name__, url_prefix="/api/contacts")


@bp.get("")
@require_auth
def list_contacts():
    rows = ContactRequest.query.filter(
        ((ContactRequest.sender_id == g.user.id) | (ContactRequest.recipient_id == g.user.id)),
        ContactRequest.status == "accepted").all()
    ids = {r.recipient_id if r.sender_id == g.user.id else r.sender_id for r in rows}
    users = User.query.filter(User.id.in_(ids)).all() if ids else []
    return jsonify(contacts=[profile(u) for u in users])


def profile(u):
    return {"id": u.id, "astra_id": u.astra_id, "astra_id_display": format_astra_id(u.astra_id),
            "username": u.username, "display_name": u.display_name, "avatar": u.avatar,
            "theme": u.theme, "settings": u.settings or {}}


@bp.post("/requests")
@require_auth
def request_contact():
    data = request.get_json(silent=True) or {}
    aid = normalize_astra_id(data.get("astra_id") or data.get("query"))
    target = User.query.filter_by(astra_id=aid).first() if aid else None
    if not target or target.id == g.user.id:
        return jsonify(error="invalid contact"), 400
    existing = ContactRequest.query.filter_by(sender_id=g.user.id, recipient_id=target.id).first()
    reverse = ContactRequest.query.filter_by(sender_id=target.id, recipient_id=g.user.id).first()
    if existing or reverse:
        return jsonify(error="request already exists"), 409
    row = ContactRequest(sender_id=g.user.id, recipient_id=target.id)
    db.session.add(row); db.session.commit()
    return jsonify(id=row.id, status=row.status), 201


@bp.post("/requests/<request_id>/accept")
@require_auth
def accept(request_id):
    row = ContactRequest.query.get_or_404(request_id)
    if row.recipient_id != g.user.id or row.status != "pending":
        return jsonify(error="not allowed"), 403
    row.status = "accepted"; db.session.commit()
    return jsonify(ok=True)


@bp.post("/<request_id>/accept")
@require_auth
def accept_alias(request_id):
    return accept(request_id)


@bp.get("/requests")
@require_auth
def requests():
    rows = ContactRequest.query.filter_by(recipient_id=g.user.id, status="pending").all()
    return jsonify(requests=[{"id": r.id, "sender": profile(User.query.get(r.sender_id))} for r in rows])


@bp.post("/requests/<request_id>/decline")
@require_auth
def decline(request_id):
    row = ContactRequest.query.get_or_404(request_id)
    if row.recipient_id != g.user.id or row.status != "pending":
        return jsonify(error="not allowed"), 403
    row.status = "declined"
    db.session.commit()
    return jsonify(ok=True)
