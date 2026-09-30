from flask import Blueprint, render_template, request, session

from app.services.file_integrity import (
    calculate_bytes_hash,
    check_file_integrity
)

from app.services.database import get_db_connection
from app.utils.auth import login_required


file_integrity_bp = Blueprint(
    "file_integrity",
    __name__,
    url_prefix="/file-integrity"
)


@file_integrity_bp.route("/", methods=["GET", "POST"])
@login_required
def file_integrity():

    user_id = session["user_id"]
    result = None

    if request.method == "POST":

        file = request.files.get("file")

        if not file or not file.filename:

            result = {
                "status": "ERROR",
                "message": "Please select a file."
            }

        else:

            file_data = file.read()

            current_hash = calculate_bytes_hash(file_data)

            filename = file.filename

            connection = get_db_connection()

            baseline = connection.execute(
                """
                SELECT file_hash
                FROM file_integrity_baselines
                WHERE user_id = ? AND filename = ?
                """,
                (user_id, filename)
            ).fetchone()

            if baseline is None:

                connection.execute(
                    """
                    INSERT INTO file_integrity_baselines
                    (user_id, filename, file_hash)
                    VALUES (?, ?, ?)
                    """,
                    (
                        user_id,
                        filename,
                        current_hash
                    )
                )

                connection.commit()
                connection.close()

                result = {
                    "status": "BASELINE",
                    "message": "Baseline hash created for this file.",
                    "hash": current_hash
                }

            else:

                original_hash = baseline["file_hash"]

                connection.close()

                result = check_file_integrity(
                    current_hash,
                    original_hash
                )

    return render_template(
        "file_integrity.html",
        result=result
    )