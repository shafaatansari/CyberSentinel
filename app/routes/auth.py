from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

import sqlite3

from app.services.database import get_db_connection
from app.services.event_service import create_event
from app.services.alert_service import create_alert


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            return render_template(
                "register.html",
                error="Username and password are required."
            )

        if len(password) < 8:
            return render_template(
                "register.html",
                error="Password must be at least 8 characters."
            )

        password_hash = generate_password_hash(password)

        connection = get_db_connection()

        try:

            connection.execute(
                """
                INSERT INTO users
                (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )

            connection.commit()

        except sqlite3.IntegrityError:

            connection.close()

            return render_template(
                "register.html",
                error="Username already exists."
            )

        connection.close()

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        connection = get_db_connection()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE username = ?
            """,
            (username,)
        ).fetchone()

        connection.close()

        # Successful login
        if user and check_password_hash(
            user["password_hash"],
            password
        ):

            session["user_id"] = user["id"]
            session["username"] = user["username"]

            create_event(
                "LOGIN_SUCCESS",
                f"Successful login for user: {username}",
                "low",
                user["id"]
            )

            return redirect(url_for("main.dashboard"))

        # Failed login
        failed_user_id = user["id"] if user else None

        create_event(
            "LOGIN_FAILED",
            f"Failed login attempt for user: {username}",
            "medium",
            failed_user_id
        )

        # Check repeated failed attempts
        if failed_user_id:

            connection = get_db_connection()

            failed_attempts = connection.execute(
                """
                SELECT COUNT(*)
                FROM security_events
                WHERE user_id = ?
                  AND event_type = 'LOGIN_FAILED'
                  AND created_at >= datetime('now', '-10 minutes')
                """,
                (failed_user_id,)
            ).fetchone()[0]

            existing_alert = connection.execute(
                """
                SELECT id
                FROM security_alerts
                WHERE user_id = ?
                  AND title = ?
                  AND created_at >= datetime('now', '-10 minutes')
                """,
                (
                    failed_user_id,
                    "Repeated Failed Login Attempts"
                )
            ).fetchone()

            connection.close()

            if failed_attempts >= 3 and not existing_alert:

                create_alert(
                    "Repeated Failed Login Attempts",
                    "Multiple failed login attempts were detected for your account.",
                    "high",
                    failed_user_id
                )

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():

    user_id = session.get("user_id")
    username = session.get("username")

    if user_id:

        create_event(
            "LOGOUT",
            f"User logged out: {username}",
            "low",
            user_id
        )

    session.clear()

    return redirect(url_for("auth.login"))