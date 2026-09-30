from flask import Blueprint, render_template, redirect, url_for, session

from app.services.alert_service import get_alerts
from app.services.event_service import get_events
from app.services.database import get_db_connection
from app.services.security_score import calculate_security_score
from app.utils.auth import login_required


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def home():

    if "user_id" in session:
        return redirect(url_for("main.dashboard"))

    return redirect(url_for("auth.login"))


@main_bp.route("/dashboard")
@login_required
def dashboard():

    user_id = session["user_id"]

    alerts = get_alerts(user_id)
    events = get_events(user_id)

    connection = get_db_connection()

    event_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM security_events
        WHERE user_id = ?
        """,
        (user_id,)
    ).fetchone()[0]

    failed_login_count = connection.execute(
        """
        SELECT COUNT(*)
        FROM security_events
        WHERE user_id = ?
          AND event_type = 'LOGIN_FAILED'
          AND created_at >= datetime('now', '-10 minutes')
        """,
        (user_id,)
    ).fetchone()[0]

    connection.close()

    alert_count = len(alerts)

    security_score = calculate_security_score(
        event_count,
        alert_count,
        failed_login_count
    )

    return render_template(
        "dashboard.html",
        alert_count=alert_count,
        event_count=event_count,
        events=events,
        security_score=security_score,
        username=session.get("username")
    )


@main_bp.route("/settings")
@login_required
def settings():

    return render_template("settings.html")