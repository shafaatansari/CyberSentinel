from app.services.database import get_db_connection


def initialize_database():

    connection = get_db_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS security_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS security_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            severity TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS file_integrity_baselines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            file_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, filename),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Existing database ke liye migration
    event_columns = connection.execute(
        "PRAGMA table_info(security_events)"
    ).fetchall()

    event_column_names = [column["name"] for column in event_columns]

    if "user_id" not in event_column_names:
        connection.execute(
            "ALTER TABLE security_events ADD COLUMN user_id INTEGER"
        )

    alert_columns = connection.execute(
        "PRAGMA table_info(security_alerts)"
    ).fetchall()

    alert_column_names = [column["name"] for column in alert_columns]

    if "user_id" not in alert_column_names:
        connection.execute(
            "ALTER TABLE security_alerts ADD COLUMN user_id INTEGER"
        )

    connection.commit()
    connection.close()