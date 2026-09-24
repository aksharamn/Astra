import logging
from flask import request
from flask_socketio import emit, join_room
from security.sessions import current_user
from .messaging import connected, create_message, serialize


def register_socket_events(socketio):
    online = set()
    security_log = logging.getLogger("astra.security")

    @socketio.on("connect")
    def connected_event():
        user = current_user()
        if not user:
            security_log.warning("unauthenticated socket connection rejected from %s", request.remote_addr or "unknown")
            return False
        join_room(user.id)
        online.add(user.id)
        emit("ready", {"user_id": user.id})
        emit("presence", {"user_id": user.id, "online": True}, broadcast=True)

    @socketio.on("disconnect")
    def disconnected_event():
        user = current_user()
        if user:
            online.discard(user.id)
            emit("presence", {"user_id": user.id, "online": False}, broadcast=True)

    @socketio.on("typing")
    def typing_event(data):
        user = current_user()
        if user and isinstance(data, dict) and connected(user.id, data.get("recipient_id") or data.get("conversation_id")):
            emit("typing", {"user_id": user.id, "typing": bool(data.get("typing"))},
                 room=data.get("recipient_id") or data.get("conversation_id"))

    @socketio.on("message:read")
    def read_event(data):
        user = current_user()
        if not user or not isinstance(data, dict):
            return
        from database.models import Message
        from database.db import db
        from datetime import datetime, timezone
        msg = Message.query.get(data.get("message_id"))
        if msg and msg.recipient_id == user.id:
            msg.delivery_status = "read"; msg.read_at = datetime.now(timezone.utc)
            db.session.commit()
            emit("message:read", {"message_id": msg.id}, room=msg.sender_id)

    @socketio.on("message:send")
    def send_event(data):
        user = current_user()
        if not user or not isinstance(data, dict):
            return
        recipient = data.get("recipient_id") or data.get("conversation_id")
        if not connected(user.id, recipient):
            emit("message:error", {"error": "contact required"})
            return
        try:
            message = create_message(user.id, recipient, data.get("message") or data.get("body"))
        except ValueError as exc:
            emit("message:error", {"error": str(exc)})
            return
        payload = serialize(message)
        packet = {"id": message.id, "protocol": "Socket.IO/WebSocket over TCP",
                  "source": request.remote_addr, "destination": None,
                  "encrypted": payload["encrypted"], "timestamp": payload["created_at"],
                  "integrity": "AES-256-GCM authentication tag"}
        for layer, detail in ((7, "message created"), (6, "AES-256-GCM encryption"),
                              (5, "secure session"), (4, "Socket.IO/TCP transport"),
                              (3, "LAN IP routing"), (2, "Wi-Fi/Ethernet frame (SIMULATED)"),
                              (1, "physical transmission (SIMULATED)")):
            emit("osi:event", {"message_id": message.id, "direction": "send",
                               "layer": layer, "detail": detail}, room=user.id)
        for layer, detail in ((1, "physical transmission (SIMULATED)"),
                              (2, "Wi-Fi/Ethernet frame (SIMULATED)"),
                              (3, "LAN IP routing"), (4, "Socket.IO/TCP transport"),
                              (5, "secure session"), (6, "AES-256-GCM authentication"),
                              (7, "message delivered")):
            emit("osi:event", {"message_id": message.id, "direction": "receive",
                               "layer": layer, "detail": detail}, room=recipient)
        emit("packet", packet, room=user.id)
        emit("packet", packet, room=recipient)
        emit("message:new", payload, room=recipient)
        emit("message:sent", payload)
