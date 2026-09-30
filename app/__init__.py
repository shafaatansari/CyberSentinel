from flask import Flask


def create_app():
    app = Flask(__name__)

    import os
    from dotenv import load_dotenv

    load_dotenv()

    app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "cybersentinel-development-secret"
    )

    from app.routes.main import main_bp
    app.register_blueprint(main_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.alerts import alerts_bp
    app.register_blueprint(alerts_bp)

    from app.routes.events import events_bp
    app.register_blueprint(events_bp)

    from app.routes.password import password_bp
    app.register_blueprint(password_bp)

    from app.routes.url_analyzer import url_analyzer_bp
    app.register_blueprint(url_analyzer_bp)

    from app.routes.file_integrity import file_integrity_bp
    app.register_blueprint(file_integrity_bp)

    from app.routes.security_score import security_score_bp
    app.register_blueprint(security_score_bp)

    from app.services.database_init import initialize_database
    initialize_database()

    return app