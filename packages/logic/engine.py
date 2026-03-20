from packages.core.models import ThreatAlert, UserAlert
from datetime import datetime

def convert_to_user_alert(threat: ThreatAlert) -> UserAlert:
    # Use the file path from the threat if available
    file_name = threat.file_path.split("\\")[-1] if threat.file_path else "Unknown File"
    
    return UserAlert(
        timestamp=datetime.now(),
        title="Malware Blocked",
        why_blocked=f"Threat {threat.threat_name} was found in {file_name}.", # Added file name here
        explanation="This file contains a signature used for security testing. It has been isolated to keep your system safe.",
        recommended_steps=["Delete the file", "Run a full scan"],
        severity="High",
        file_path=threat.file_path,
        threat_name=threat.threat_name
    )