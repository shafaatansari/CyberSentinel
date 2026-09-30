from flask import Blueprint, render_template, request, session

from app.services.password_service import check_password_strength
from app.utils.auth import login_required


password_bp = Blueprint(
    "password",
    __name__,
    url_prefix="/password"
)


@password_bp.route("/", methods=["GET", "POST"])
@login_required
def password_security():

    result = None

    if request.method == "POST":

        password = request.form.get("password", "")

        result = check_password_strength(password)

    return render_template(
        "password.html",
        result=result
    )