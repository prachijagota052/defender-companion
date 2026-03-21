import time

from packages.core.db import (
    fetch_unprocessed_threat_alerts,
    insert_user_alert,
    mark_threat_processed,
)
from packages.logic.engine import convert_to_user_alert


def process_once():
    threats = fetch_unprocessed_threat_alerts(limit=20)

    for threat in threats:
        try:
            user_alert = convert_to_user_alert(threat)
            user_alert_id = insert_user_alert(user_alert)
            mark_threat_processed(threat.id)

            print(
                f"[RUNNER] Processed threat_id={threat.id} -> user_alert_id={user_alert_id}"
            )
        except Exception as e:
            print(f"[RUNNER ERROR] threat_id={threat.id} | {e}")


def main():
    print("[RUNNER] Running continuously...")

    try:
        while True:
            process_once()
            time.sleep(1)
    except KeyboardInterrupt:
        print("[RUNNER] Stopped.")


if __name__ == "__main__":
    main()