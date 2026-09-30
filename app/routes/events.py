from flask import Blueprint, render_template, session

from app.services.event_service import get_events
from app.utils.auth import login_required


events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events"
)


@events_bp.route("/")
@login_required
def events():

    user_id = session["user_id"]

    events = get_events(user_id)

    return render_template(
        "events.html",
        events=events
    )