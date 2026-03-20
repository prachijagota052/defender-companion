from datetime import datetime
from packages.core.models import ThreatAlert
from packages.core.db import insert_threat_alert

def trigger():
    print("🚀 Connecting to internal DB logic...")
    
    # Create a ThreatAlert object using your Pydantic model
    mock_threat = ThreatAlert(
        timestamp=datetime.now(),
        source_type="Antivirus",
        file_path="C:\\Users\\DELL\\Downloads\\eicar_test.com",
        threat_name="Trojan:Win32/Eicar.C",
        action_taken="Blocked",
        severity="High",
        raw_message='{"event_id": 1116, "engine": "Defender"}'
    )

    try:
        # This automatically calls init_db() and handles the 'data' folder
        alert_id = insert_threat_alert(mock_threat)
        print(f"✅ SUCCESS: Threat inserted with ID: {alert_id}")
        print("📢 The Runner and Audio Service should react now!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    trigger()