# packages/logic/runner.py

from packages.core.db import get_unprocessed_alerts, insert_user_alert, mark_alert_processed
from apps.logic.engine import convert_to_user_alert


def process_alerts():
    alerts = get_unprocessed_alerts()

    for alert in alerts:
        try:
            user_alert = convert_to_user_alert(alert)
            insert_user_alert(user_alert)
            mark_alert_processed(alert.id)

            print(f"Processed alert {alert.id}")

        except Exception as e:
            print(f"Error processing alert {alert.id}: {e}")


if __name__ == "__main__":
    process_alerts()
