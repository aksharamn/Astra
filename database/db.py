from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import NullPool

db = SQLAlchemy()


def init_db(app):
    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:") and "SQLALCHEMY_ENGINE_OPTIONS" not in app.config:
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"poolclass": NullPool}
    db.init_app(app)
    with app.app_context():
        from . import models  # noqa: F401
        db.create_all()
        if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:"):
            columns = {row[1] for row in db.session.execute(db.text("PRAGMA table_info(user)"))}
            if "email" not in columns:
                db.session.execute(db.text("ALTER TABLE user ADD COLUMN email VARCHAR(254)"))
                db.session.commit()
        legacy_users = models.User.query.all()
        changed = False
        for user in legacy_users:
            if len(user.astra_id or "") != 12:
                candidate = models.generate_astra_id()
                while models.User.query.filter_by(astra_id=candidate).first():
                    candidate = models.generate_astra_id()
                user.astra_id = candidate
                changed = True
        if changed:
            db.session.commit()
