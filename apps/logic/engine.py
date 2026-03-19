# packages/logic/engine.py

from packages.core.models import ThreatAlert, UserAlert
from apps.logic.rules import THREAT_RULES
from datetime import datetime


def match_rule(alert: ThreatAlert):
    if alert.threat_name:
        name = alert.threat_name.lower()

        for keyword, rule in THREAT_RULES.items():
            if keyword in name:
                return rule

    # Fallback rule
    return {
        "title": "Security Alert",
        "why": "Windows blocked a file due to security concerns.",
        "explanation": "The file was prevented from running to protect your system.",
        "steps": ["No action required."],
        "severity": "Info"
    }


def convert_to_user_alert(alert: ThreatAlert) -> UserAlert:
    rule = match_rule(alert)

    return UserAlert(
        timestamp=datetime.now(),
        title=rule["title"],
        why_blocked=rule["why"],
        explanation=rule["explanation"],
        recommended_steps=rule["steps"],
        severity=rule["severity"],
        file_path=alert.file_path,
        threat_name=alert.threat_name,
        source_type=alert.source_type
    )
