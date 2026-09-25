import hashlib
import hmac
import json
from dotenv import load_dotenv

# Load .env before importing Config so ASTRA_MASTER_KEY and ASTRA_SECRET_KEY
# are available when the Config class is created.
load_dotenv()

from flask import Flask, jsonify, g, request, render_template
from flask_socketio import SocketIO
from config import Config
from database.db import init_db
from database.models import User, Message, ContactRequest
from security.keys import master_key
from security.sessions import require_auth
from backend.auth import bp as auth_bp
from backend.profiles import bp as profiles_bp
from backend.contacts import bp as contacts_bp
from backend.messaging import bp as messaging_bp
from backend.websocket import register_socket_events


def create_app(config_object=None):
    app = Flask(__name__)
    app.config.from_object(config_object or Config)

    init_db(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(messaging_bp)

    allowed_origins = app.config.get("ASTRA_ALLOWED_ORIGINS", ())

    socketio = SocketIO(
        app,
        cors_allowed_origins=list(allowed_origins),
        async_mode="threading",
    )

    register_socket_events(socketio)

    @app.after_request
    def security_headers(response):
        origin = request.headers.get("Origin")

        if origin and origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Vary"] = "Origin"

        response.headers.setdefault("X-Content-Type-Options", "nosniff")
        response.headers.setdefault("X-Frame-Options", "DENY")
        response.headers.setdefault(
            "Referrer-Policy",
            "strict-origin-when-cross-origin",
        )
        response.headers.setdefault(
            "Content-Security-Policy",
            "default-src 'self'; "
            "connect-src 'self' https://cdn.socket.io ws: wss:; "
            "script-src 'self' 'unsafe-inline' https://cdn.socket.io; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:;",
        )

        return response

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api/health")
    def health():
        return jsonify(ok=True, service="astra")

    @app.get("/api/me")
    @require_auth
    def me_alias():
        u = g.user

        from backend.auth import user_json

        result = user_json(u)
        result["bio"] = u.bio

        return jsonify(user=result)

    @app.get("/api/conversations")
    @require_auth
    def conversations_alias():
        rows = ContactRequest.query.filter(
            (
                (ContactRequest.sender_id == g.user.id)
                | (ContactRequest.recipient_id == g.user.id)
            ),
            ContactRequest.status == "accepted",
        ).all()

        ids = {
            r.recipient_id if r.sender_id == g.user.id else r.sender_id
            for r in rows
        }

        users = User.query.filter(User.id.in_(ids)).all() if ids else []

        return jsonify(
            conversations=[
                {
                    "id": u.id,
                    "astra_id": u.astra_id,
                    "username": u.username,
                    "display_name": u.display_name,
                    "avatar": u.avatar,
                    "astra_id_display": (
                        f"ASTRA-{u.astra_id[:4]}-"
                        f"{u.astra_id[4:8]}-"
                        f"{u.astra_id[8:]}"
                    ),
                }
                for u in users
            ]
        )

    @app.route(
        "/api/conversations/<user_id>/messages",
        methods=["GET", "POST"],
    )
    @require_auth
    def conversation_messages_alias(user_id):
        from backend.messaging import history, send

        if request.method == "GET":
            return history(user_id)

        return send(user_id)

    @app.get("/api/tamper")
    @require_auth
    def tamper():
        # A deterministic authenticated digest lets an operator detect row changes.
        rows = []

        for model in (User, ContactRequest, Message):
            for row in model.query.order_by(model.id).all():
                values = {
                    c.name: str(getattr(row, c.name))
                    for c in model.__table__.columns
                }

                rows.append(
                    model.__tablename__
                    + ":"
                    + json.dumps(
                        values,
                        sort_keys=True,
                        default=str,
                    )
                )

        digest = hmac.new(
            master_key(app.config),
            "\n".join(rows).encode(),
            hashlib.sha256,
        ).hexdigest()

        expected = request.args.get("digest")

        if not expected:
            expected = (request.get_json(silent=True) or {}).get("digest")

        return jsonify(
            algorithm="HMAC-SHA256",
            digest=digest,
            rows=len(rows),
            valid=(
                hmac.compare_digest(digest, expected)
                if expected
                else None
            ),
        )

    app.extensions["socketio"] = socketio

    return app


app = create_app()


if __name__ == "__main__":
    app.extensions["socketio"].run(
        app,
        host="0.0.0.0",
        port=int(__import__("os").getenv("PORT", "5000")),
    )
