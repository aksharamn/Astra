from flask import Blueprint, jsonify, request, g
from cryptography.exceptions import InvalidTag
from database.db import db
from database.models import ContactRequest, Message, User
from security.encryption import encrypt_payload, decrypt_payload
from security.sessions import require_auth

bp = Blueprint("messaging", __name__, url_prefix="/api/messages")


def connected(a, b):
    return ContactRequest.query.filter(
        (((ContactRequest.sender_id == a) & (ContactRequest.recipient_id == b)) |
         ((ContactRequest.sender_id == b) & (ContactRequest.recipient_id == a))),
        ContactRequest.status == "accepted").first() is not None


def serialize(message, decrypt_content=True):
    payload = {"ciphertext": message.ciphertext, "nonce": message.nonce, "tag": message.tag}
    text = decrypt_payload(payload) if decrypt_content else None
    return {"id": message.id, "sender_id": message.sender_id, "recipient_id": message.recipient_id,
            "message": text, "body": text, "content": text,
            "created_at": message.created_at.isoformat(), "delivery_status": message.delivery_status,
            "read_at": message.read_at.isoformat() if message.read_at else None,
            "encrypted": payload}


@bp.get("/<user_id>")
@require_auth
def history(user_id):
    if not User.query.get(user_id) or not connected(g.user.id, user_id):
        return jsonify(error="contact required"), 403
    rows = Message.query.filter(
        (((Message.sender_id == g.user.id) & (Message.recipient_id == user_id)) |
         ((Message.sender_id == user_id) & (Message.recipient_id == g.user.id)))).order_by(Message.created_at).limit(100).all()
    return jsonify(messages=[serialize(x) for x in rows])


def create_message(sender, recipient, text):
    if not isinstance(text, str) or not text.strip() or len(text) > 4000:
        raise ValueError("invalid message")
    payload = encrypt_payload(text)
    row = Message(sender_id=sender, recipient_id=recipient, **payload)
    db.session.add(row); db.session.commit()
    return row


@bp.post("/<user_id>")
@require_auth
def send(user_id):
    if not connected(g.user.id, user_id):
        return jsonify(error="contact required"), 403
    try:
        data = request.get_json(silent=True) or {}
        row = create_message(g.user.id, user_id, data.get("message") or data.get("body"))
    except ValueError as e:
        return jsonify(error=str(e)), 400
    return jsonify(message=serialize(row)), 201


@bp.get("/conversations")
@require_auth
def conversations():
    rows = ContactRequest.query.filter(
        ((ContactRequest.sender_id == g.user.id) | (ContactRequest.recipient_id == g.user.id)),
        ContactRequest.status == "accepted").all()
    ids = {r.recipient_id if r.sender_id == g.user.id else r.sender_id for r in rows}
    users = User.query.filter(User.id.in_(ids)).all() if ids else []
    return jsonify(conversations=[{"id": u.id, "username": u.username, "display_name": u.display_name} for u in users])


@bp.get("/conversations/<user_id>/messages")
@bp.post("/conversations/<user_id>/messages")
@require_auth
def conversation_messages(user_id):
    if request.method == "GET":
        return history(user_id)
    return send(user_id)


@bp.post("/tamper")
@require_auth
def verify_tampered_packet():
    data = request.get_json(silent=True) or {}
    payload = data.get("encrypted") or data
    try:
        decrypt_payload(payload)
    except (InvalidTag, ValueError, KeyError, TypeError):
        return jsonify(valid=False, error="integrity check failed"), 400
    return jsonify(valid=True)
