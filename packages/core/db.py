import sqlite3
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import json

from .models import ThreatAlert, UserAlert

# DB file path: repo_root/data/companion.db
DB_PATH = Path(__file__).resolve().parents[2] / "data" / "companion.db"


def get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Create required tables if they don't exist."""
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS threat_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source_type TEXT NOT NULL,
                file_path TEXT,
                threat_name TEXT,
                action_taken TEXT,
                severity TEXT,
                raw_message TEXT,
                processed INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                title TEXT NOT NULL,
                why_blocked TEXT NOT NULL,
                explanation TEXT NOT NULL,
                recommended_steps TEXT NOT NULL,  -- JSON list
                severity TEXT NOT NULL,
                file_path TEXT,
                threat_name TEXT,
                source_type TEXT,
                spoken INTEGER NOT NULL DEFAULT 0
            );
            """
        )


# ----------------------------
# Threat alerts (Member 1 -> DB)
# ----------------------------
def insert_threat_alert(alert: ThreatAlert) -> int:
    init_db()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO threat_alerts
            (timestamp, source_type, file_path, threat_name, action_taken, severity, raw_message, processed)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                alert.timestamp.isoformat(),
                alert.source_type,
                alert.file_path,
                alert.threat_name,
                alert.action_taken,
                alert.severity,
                alert.raw_message,
            ),
        )
        return int(cur.lastrowid)


def fetch_unprocessed_threat_alerts(limit: int = 50) -> List[ThreatAlert]:
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT * FROM threat_alerts
            WHERE processed = 0
            ORDER BY id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    alerts: List[ThreatAlert] = []
    for r in rows:
        alerts.append(
            ThreatAlert(
                id=r["id"],
                timestamp=datetime.fromisoformat(r["timestamp"]),
                source_type=r["source_type"],
                file_path=r["file_path"],
                threat_name=r["threat_name"],
                action_taken=r["action_taken"],
                severity=r["severity"],
                raw_message=r["raw_message"],
            )
        )
    return alerts


def mark_threat_processed(threat_id: int) -> None:
    init_db()
    with get_conn() as conn:
        conn.execute(
            "UPDATE threat_alerts SET processed = 1 WHERE id = ?",
            (threat_id,),
        )


# ----------------------------
# User alerts (Member 2 -> DB; UI + Audio read)
# ----------------------------
def insert_user_alert(alert: UserAlert) -> int:
    init_db()
    with get_conn() as conn:
        cur = conn.execute(
            """
            INSERT INTO user_alerts
            (timestamp, title, why_blocked, explanation, recommended_steps, severity,
             file_path, threat_name, source_type, spoken)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
            """,
            (
                alert.timestamp.isoformat(),
                alert.title,
                alert.why_blocked,
                alert.explanation,
                json.dumps(alert.recommended_steps, ensure_ascii=False),
                alert.severity,
                alert.file_path,
                alert.threat_name,
                alert.source_type,
            ),
        )
        return int(cur.lastrowid)


def fetch_latest_user_alerts(limit: int = 50) -> List[UserAlert]:
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT * FROM user_alerts
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    alerts: List[UserAlert] = []
    for r in rows:
        alerts.append(
            UserAlert(
                id=r["id"],
                timestamp=datetime.fromisoformat(r["timestamp"]),
                title=r["title"],
                why_blocked=r["why_blocked"],
                explanation=r["explanation"],
                recommended_steps=json.loads(r["recommended_steps"]),
                severity=r["severity"],
                file_path=r["file_path"],
                threat_name=r["threat_name"],
                source_type=r["source_type"],
            )
        )
    return alerts


def fetch_unspoken_user_alerts(limit: int = 20) -> List[UserAlert]:
    """For Member 4 (audio): get alerts that haven't been spoken yet."""
    init_db()
    with get_conn() as conn:
        rows = conn.execute(
            """
            SELECT * FROM user_alerts
            WHERE spoken = 0
            ORDER BY id ASC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    alerts: List[UserAlert] = []
    for r in rows:
        alerts.append(
            UserAlert(
                id=r["id"],
                timestamp=datetime.fromisoformat(r["timestamp"]),
                title=r["title"],
                why_blocked=r["why_blocked"],
                explanation=r["explanation"],
                recommended_steps=json.loads(r["recommended_steps"]),
                severity=r["severity"],
                file_path=r["file_path"],
                threat_name=r["threat_name"],
                source_type=r["source_type"],
            )
        )
    return alerts


def mark_user_alert_spoken(user_alert_id: int) -> None:
    """For Member 4: mark alert as spoken so it won't repeat."""
    init_db()
    with get_conn() as conn:
        conn.execute(
            "UPDATE user_alerts SET spoken = 1 WHERE id = ?",
            (user_alert_id,),
        )
