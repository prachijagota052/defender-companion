import json
from datetime import datetime

from packages.core.models import ThreatAlert, UserAlert
from packages.logic.rules import THREAT_RULES


def detect_rule_key(threat_name: str) -> str | None:
    if not threat_name:
        return None

    value = threat_name.lower()

    if "eicar" in value:
        return "eicar"
    if "pua" in value:
        return "pua"
    if "trojan" in value or "ransom" in value or "worm" in value:
        return "trojan"

    return None


def safe_filename(path: str | None) -> str:
    if not path:
        return "Unknown File"
    return path.replace("/", "\\").split("\\")[-1]


def build_default_alert(threat: ThreatAlert) -> UserAlert:
    file_name = safe_filename(threat.file_path)

    return UserAlert(
        timestamp=datetime.now(),
        title="Threat Detected",
        why_blocked=f"Microsoft Defender detected {threat.threat_name or 'a suspicious item'} in {file_name}.",
        explanation="Windows Defender identified this item and blocked or logged it to help protect your PC.",
        recommended_steps=[
            "Do not open or run the file again.",
            "Open Windows Security and review Protection history.",
            "Run a quick or full scan."
        ],
        severity=threat.severity or "High",
        file_path=threat.file_path,
        threat_name=threat.threat_name,
        source_type=threat.source_type,
    )


def build_settings_change_alert(threat: ThreatAlert) -> UserAlert:
    return UserAlert(
        timestamp=datetime.now(),
        title="Windows Defender Setting Changed",
        why_blocked="A Microsoft Defender security setting was changed.",
        explanation="This does not always mean malware, but security-related settings were modified and should be reviewed.",
        recommended_steps=[
            "Open Windows Security and review recent changes.",
            "Confirm that real-time protection and other protections are still enabled.",
            "If the change was unexpected, run a scan."
        ],
        severity="Informational",
        file_path=threat.file_path,
        threat_name=threat.threat_name,
        source_type=threat.source_type,
    )


def convert_to_user_alert(threat: ThreatAlert) -> UserAlert:
    if (threat.threat_name or "").lower() == "security setting changed":
        return build_settings_change_alert(threat)

    rule_key = detect_rule_key(threat.threat_name or "")
    if rule_key and rule_key in THREAT_RULES:
        rule = THREAT_RULES[rule_key]
        file_name = safe_filename(threat.file_path)

        return UserAlert(
            timestamp=datetime.now(),
            title=rule["title"],
            why_blocked=f"{rule['why']} File: {file_name}. Threat: {threat.threat_name or 'Unknown Threat'}.",
            explanation=rule["explanation"],
            recommended_steps=rule["steps"],
            severity=rule["severity"],
            file_path=threat.file_path,
            threat_name=threat.threat_name,
            source_type=threat.source_type,
        )

    return build_default_alert(threat)