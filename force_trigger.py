from datetime import datetime
from packages.core.db import insert_threat_alert
from packages.core.models import ThreatAlert

alert = ThreatAlert(
    timestamp=datetime.now(),
    source_type="Test",
    file_path="C:\\test\\virus.exe",
    threat_name="Trojan.Test",
    action_taken="Blocked",
    severity="High",
    raw_message="Manual Test"
)

insert_threat_alert(alert)

print("✅ Test threat inserted!")