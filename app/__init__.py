from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config.config import Config


db = SQLAlchemy()


def _migrate_notifications_table(app):
    if not app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite"):
        return

    engine = db.engine
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='notifications'")
    if not cursor.fetchone():
        conn.commit()
        cursor.close()
        conn.close()
        return

    cursor.execute("PRAGMA table_info(notifications)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    desired_columns = [
        "id",
        "title",
        "message",
        "recipient",
        "notification_type",
        "priority",
        "status",
        "created_at",
    ]

    if existing_columns == desired_columns:
        conn.commit()
        cursor.close()
        conn.close()
        return

    cursor.execute("ALTER TABLE notifications RENAME TO notifications_old")
    cursor.execute(
        """
        CREATE TABLE notifications (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            recipient TEXT NOT NULL,
            notification_type TEXT NOT NULL DEFAULT 'In-App',
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Unread',
            created_at TEXT NOT NULL
        )
        """
    )

    def column_expr(name, default):
        if name in existing_columns:
            return f"COALESCE({name}, {default})"
        return default

    insert_columns = ", ".join(desired_columns)
    select_expressions = [
        column_expr("id", "NULL"),
        column_expr("title", "'Notification'"),
        column_expr("message", "''"),
        column_expr("recipient", "'All Members'"),
        column_expr("notification_type", "'In-App'"),
        column_expr("priority", "'Medium'"),
        column_expr("status", "'Unread'"),
        column_expr("created_at", "'" + datetime.utcnow().strftime("%Y-%m-%d %H:%M") + "'"),
    ]

    cursor.execute(
        f"INSERT INTO notifications ({insert_columns}) SELECT {', '.join(select_expressions)} FROM notifications_old"
    )
    cursor.execute("DROP TABLE notifications_old")
    conn.commit()
    cursor.close()
    conn.close()


def _migrate_settings_table(app):
    if not app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite"):
        return

    engine = db.engine
    conn = engine.raw_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='system_settings'")
    if not cursor.fetchone():
        conn.commit()
        cursor.close()
        conn.close()
        return

    cursor.execute("PRAGMA table_info(system_settings)")
    existing_columns = [row[1] for row in cursor.fetchall()]
    desired_columns = [
        "id",
        "theme",
        "items_per_page",
        "date_format",
        "email_notifications",
        "sms_notifications",
        "contribution_reminders",
        "group_updates",
        "payout_alerts",
        "meeting_reminders",
    ]

    if existing_columns == desired_columns:
        conn.commit()
        cursor.close()
        conn.close()
        return

    cursor.execute("ALTER TABLE system_settings RENAME TO system_settings_old")
    cursor.execute(
        """
        CREATE TABLE system_settings (
            id INTEGER PRIMARY KEY,
            theme TEXT NOT NULL DEFAULT 'light',
            items_per_page INTEGER NOT NULL DEFAULT 25,
            date_format TEXT NOT NULL DEFAULT 'dd/mm/yyyy',
            email_notifications INTEGER NOT NULL DEFAULT 1,
            sms_notifications INTEGER NOT NULL DEFAULT 1,
            contribution_reminders INTEGER NOT NULL DEFAULT 1,
            group_updates INTEGER NOT NULL DEFAULT 1,
            payout_alerts INTEGER NOT NULL DEFAULT 1,
            meeting_reminders INTEGER NOT NULL DEFAULT 1
        )
        """
    )

    def column_expr(name, default):
        if name in existing_columns:
            return f"COALESCE({name}, {default})"
        return default

    insert_columns = ", ".join(desired_columns)
    select_expressions = [
        column_expr("id", "NULL"),
        column_expr("theme", "'light'"),
        column_expr("items_per_page", "25"),
        column_expr("date_format", "'dd/mm/yyyy'"),
        column_expr("email_notifications", "1"),
        column_expr("sms_notifications", "1"),
        column_expr("contribution_reminders", "1"),
        column_expr("group_updates", "1"),
        column_expr("payout_alerts", "1"),
        column_expr("meeting_reminders", "1"),
    ]

    cursor.execute(
        f"INSERT INTO system_settings ({insert_columns}) SELECT {', '.join(select_expressions)} FROM system_settings_old"
    )
    cursor.execute("DROP TABLE system_settings_old")
    conn.commit()
    cursor.close()
    conn.close()


def create_app(config_overrides=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)

    from .models import Contribution, Group, Member, Notification, Payout, Settings, User
    from .routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()
        _migrate_notifications_table(app)
        _migrate_settings_table(app)

    return app
