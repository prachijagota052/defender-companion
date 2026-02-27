from datetime import datetime
from packages.core.db import (
    init_db,
    insert_threat_alert,
    insert_user_alert,
    fetch_latest_user_alerts,
)
from packages.core.models import ThreatAlert, UserAlert


def main():
    init_db()

    # 1) Insert a fake ThreatAlert (simulates Member 1 output)
    ta = ThreatAlert(
        timestamp=datetime.now(),
        source_type="DefenderAV",
        file_path=r"C:\Users\Prachi\Downloads\eicar.com.txt",
        threat_name="EICAR-Test-File",
        action_taken="Blocked",
        severity="High",
        raw_message="Smoke test threat alert",
    )
    threat_id = insert_threat_alert(ta)
    print(f"Inserted ThreatAlert id={threat_id}")

    # 2) Insert a fake UserAlert (simulates Member 2 output)
    ua = UserAlert(
        timestamp=datetime.now(),
        title="Threat Blocked",
        why_blocked="Microsoft Defender flagged this file as suspicious.",
        explanation="The file was blocked before it could run. This helps protect your PC.",
        recommended_steps=[
            "Do not open the file again.",
            "Run a quick scan in Windows Security.",
            "Delete the download if you don’t need it.",
        ],
        severity="Warning",
        file_path=ta.file_path,
        threat_name=ta.threat_name,
        source_type=ta.source_type,
    )
    user_id = insert_user_alert(ua)
    print(f"Inserted UserAlert id={user_id}")

    # 3) Read latest UserAlerts (simulates UI + Audio reading)
    latest = fetch_latest_user_alerts(limit=5)
    print("\nLatest UserAlerts:")
    for a in latest:
        print(f"- id={a.id} | {a.title} | {a.severity} | {a.file_path}")


if __name__ == "__main__":
    main()
