from flask import Blueprint, render_template, request

from app.services.url_analyzer import analyze_url
from app.utils.auth import login_required


url_analyzer_bp = Blueprint(
    "url_analyzer",
    __name__,
    url_prefix="/url-analyzer"
)


@url_analyzer_bp.route("/", methods=["GET", "POST"])
@login_required
def url_analyzer():

    result = None

    if request.method == "POST":

        url = request.form.get("url", "")

        result = analyze_url(url)

    return render_template(
        "url_analyzer.html",
        result=result
    )