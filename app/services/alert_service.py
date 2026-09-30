from app.services.database import get_db_connection


def create_alert(
    title,
    message,
    severity="medium",
    user_id=None
):
    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO security_alerts
        (user_id, title, message, severity)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            title,
            message,
            severity
        )
    )

    connection.commit()
    connection.close()


def get_alerts(user_id=None):

    connection = get_db_connection()

    if user_id is not None:

        alerts = connection.execute(
            """
            SELECT
                id,
                user_id,
                title,
                message,
                severity,
                created_at
            FROM security_alerts
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        alerts = connection.execute(
            """
            SELECT
                id,
                user_id,
                title,
                message,
                severity,
                created_at
            FROM security_alerts
            ORDER BY id DESC
            """
        ).fetchall()

    connection.close()

    return alerts