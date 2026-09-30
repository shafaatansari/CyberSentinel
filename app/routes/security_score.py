from flask import Blueprint, render_template, session

from app.services.database import get_db_connection
from app.services.alert_service import get_alerts
from app.services.event_service import get_events
from app.services.security_score import calculate_security_score
from app.utils.auth import login_required


security_score_bp = Blueprint(
    "security_score",
    __name__,
    url_prefix="/security-score"
)


@security_score_bp.route("/")
@login_required
def security_score():

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

    score_data = calculate_security_score(
        event_count,
        alert_count,
        failed_login_count
    )

    return render_template(
        "security_score.html",
        score=score_data["score"],
        status=score_data["status"],
        event_count=event_count,
        alert_count=alert_count
    )