from flask import Blueprint, render_template, session

from app.services.alert_service import get_alerts
from app.utils.auth import login_required


alerts_bp = Blueprint(
    "alerts",
    __name__,
    url_prefix="/alerts"
)


@alerts_bp.route("/")
@login_required
def alerts():

    user_id = session["user_id"]

    alerts = get_alerts(user_id)

    return render_template(
        "alerts.html",
        alerts=alerts
    )