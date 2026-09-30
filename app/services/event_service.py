from app.services.database import get_db_connection


def create_event(
    event_type,
    description,
    severity="low",
    user_id=None
):
    connection = get_db_connection()

    connection.execute(
        """
        INSERT INTO security_events
        (user_id, event_type, description, severity)
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            event_type,
            description,
            severity
        )
    )

    connection.commit()
    connection.close()


def get_events(user_id=None):

    connection = get_db_connection()

    if user_id is not None:

        events = connection.execute(
            """
            SELECT
                id,
                user_id,
                event_type,
                description,
                severity,
                created_at
            FROM security_events
            WHERE user_id = ?
            ORDER BY id DESC
            """,
            (user_id,)
        ).fetchall()

    else:

        events = connection.execute(
            """
            SELECT
                id,
                user_id,
                event_type,
                description,
                severity,
                created_at
            FROM security_events
            ORDER BY id DESC
            """
        ).fetchall()

    connection.close()

    return events