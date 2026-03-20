import os
import json
import sqlite3
from datetime import datetime

from packages.core.models import ThreatAlert, UserAlert


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "companion.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS threat_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            source_type TEXT,
            file_path TEXT,
            threat_name TEXT,
            action_taken TEXT,
            severity TEXT,
            raw_message TEXT,
            processed INTEGER DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS user_alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            title TEXT,
            why_blocked TEXT,
            explanation TEXT,
            recommended_steps TEXT,
            severity TEXT,
            file_path TEXT,
            threat_name TEXT,
            source_type TEXT,
            spoken INTEGER DEFAULT 0,
            shown INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()


def _to_iso(value):
    if isinstance(value, datetime):
        return value.isoformat()
    return str(value)


def _parse_steps(value):
    if not value:
        return []
    try:
        return json.loads(value)
    except Exception:
        return []


def row_to_threat_alert(row):
    return ThreatAlert(
        id=row["id"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        source_type=row["source_type"],
        file_path=row["file_path"],
        threat_name=row["threat_name"],
        action_taken=row["action_taken"],
        severity=row["severity"],
        raw_message=row["raw_message"],
    )


def row_to_user_alert(row):
    return UserAlert(
        id=row["id"],
        timestamp=datetime.fromisoformat(row["timestamp"]),
        title=row["title"],
        why_blocked=row["why_blocked"],
        explanation=row["explanation"],
        recommended_steps=_parse_steps(row["recommended_steps"]),
        severity=row["severity"],
        file_path=row["file_path"],
        threat_name=row["threat_name"],
        source_type=row["source_type"],
    )


def insert_threat_alert(alert: ThreatAlert):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO threat_alerts (
            timestamp, source_type, file_path, threat_name,
            action_taken, severity, raw_message, processed
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 0)
    """, (
        _to_iso(alert.timestamp),
        alert.source_type,
        alert.file_path,
        alert.threat_name,
        alert.action_taken,
        alert.severity,
        alert.raw_message,
    ))

    conn.commit()
    alert_id = cur.lastrowid
    conn.close()
    return alert_id


def fetch_unprocessed_threat_alerts(limit=20):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM threat_alerts
        WHERE processed = 0
        ORDER BY id ASC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [row_to_threat_alert(row) for row in rows]


def mark_threat_processed(threat_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE threat_alerts
        SET processed = 1
        WHERE id = ?
    """, (threat_id,))

    conn.commit()
    conn.close()


def insert_user_alert(alert: UserAlert):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO user_alerts (
            timestamp, title, why_blocked, explanation,
            recommended_steps, severity, file_path,
            threat_name, source_type, spoken, shown
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0)
    """, (
        _to_iso(alert.timestamp),
        alert.title,
        alert.why_blocked,
        alert.explanation,
        json.dumps(alert.recommended_steps or []),
        alert.severity,
        alert.file_path,
        alert.threat_name,
        alert.source_type,
    ))

    conn.commit()
    alert_id = cur.lastrowid
    conn.close()
    return alert_id


def fetch_unspoken_user_alerts(limit=1):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM user_alerts
        WHERE spoken = 0
        ORDER BY id ASC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [row_to_user_alert(row) for row in rows]


def mark_user_alert_spoken(alert_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_alerts
        SET spoken = 1
        WHERE id = ?
    """, (alert_id,))

    conn.commit()
    conn.close()


def fetch_unshown_user_alert():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM user_alerts
        WHERE shown = 0
        ORDER BY id ASC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return row_to_user_alert(row)


def mark_user_alert_shown(alert_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_alerts
        SET shown = 1
        WHERE id = ?
    """, (alert_id,))

    conn.commit()
    conn.close()