import json
import time
import xml.etree.ElementTree as ET
from datetime import datetime

import win32evtlog

from packages.core.db import insert_threat_alert
from packages.core.models import ThreatAlert

LOG_PATH = "Microsoft-Windows-Windows Defender/Operational"
NS = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}


def is_real_threat_event(event_id, data):
    threat_name = data.get("Threat Name") or data.get("ThreatName")

    # Real malware / threat detections
    if threat_name and threat_name.lower() not in ["", "unknown"]:
        return True

    # Important Defender threat/remediation actions
    if event_id in {"1116", "1117", "1121", "1125"}:
        return True

    return False


def extract_event_data(root):
    data_dict = {}
    event_data = root.find("ns:EventData", NS)

    if event_data is not None:
        for data in event_data.findall("ns:Data", NS):
            name = data.attrib.get("Name")
            value = data.text or ""
            if name:
                data_dict[name] = value

    return data_dict


def pick_first(data_dict, keys, default=""):
    for key in keys:
        value = data_dict.get(key)
        if value:
            return value
    return default


def build_alert_from_event(event_id: str, data: dict) -> ThreatAlert:
    threat_name = pick_first(
        data,
        ["Threat Name", "ThreatName", "Name"],
        "Unknown Threat",
    )

    file_path = pick_first(
        data,
        ["Path", "File Path", "Process Name", "Detection Source"],
        "Unknown Path",
    )

    action_taken = pick_first(
        data,
        ["Action Name", "Action", "Status Description"],
        "Detected",
    )

    if "trojan" in threat_name.lower() or "ransom" in threat_name.lower():
        severity = "Critical"
    elif "pua" in threat_name.lower():
        severity = "Warning"
    else:
        severity = "High"

    return ThreatAlert(
        timestamp=datetime.now(),
        source_type="WindowsDefenderEventLog",
        file_path=file_path,
        threat_name=threat_name,
        action_taken=action_taken,
        severity=severity,
        raw_message=json.dumps(
            {"event_id": event_id, "event_data": data},
            ensure_ascii=False,
        ),
    )


def get_record_id(root):
    node = root.find("ns:System/ns:EventRecordID", NS)
    if node is None or not node.text:
        return None
    try:
        return int(node.text.strip())
    except Exception:
        return None


def get_event_id(root):
    node = root.find("ns:System/ns:EventID", NS)
    if node is None or not node.text:
        return None
    return node.text.strip()


def get_latest_record_id():
    """
    Read the current newest event once at startup so we only process
    events that happen AFTER the monitor starts.
    """
    try:
        handle = win32evtlog.EvtQuery(
            LOG_PATH,
            win32evtlog.EvtQueryReverseDirection,
            "*",
        )
        events = win32evtlog.EvtNext(handle, 1)
        if not events:
            return 0

        xml_data = win32evtlog.EvtRender(events[0], win32evtlog.EvtRenderEventXml)
        root = ET.fromstring(xml_data)
        return get_record_id(root) or 0
    except Exception as e:
        print(f"[MONITOR INIT ERROR] {e}")
        return 0


def main():
    print("[MONITOR] Watching Defender continuously...")

    last_record_id = get_latest_record_id()
    print(f"[MONITOR] Starting after record_id={last_record_id}")

    while True:
        try:
            handle = win32evtlog.EvtQuery(
                LOG_PATH,
                win32evtlog.EvtQueryReverseDirection,
                "*",
            )

            events = win32evtlog.EvtNext(handle, 20)
            if not events:
                time.sleep(1)
                continue

            parsed = []
            for event in events:
                xml_data = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
                root = ET.fromstring(xml_data)
                record_id = get_record_id(root)
                event_id = get_event_id(root)

                if record_id is not None and event_id is not None:
                    parsed.append((record_id, event_id, root))

            parsed.sort(key=lambda x: x[0])

            for record_id, event_id, root in parsed:
                if record_id <= last_record_id:
                    continue

                last_record_id = record_id
                print(f"[MONITOR DEBUG] record_id={record_id} event_id={event_id}")

                data = extract_event_data(root)

                if not is_real_threat_event(event_id, data):
                    continue

                alert = build_alert_from_event(event_id, data)
                alert_id = insert_threat_alert(alert)

                print(
                    f"[MONITOR] Saved threat_alert id={alert_id} | "
                    f"event_id={event_id} | threat={alert.threat_name}"
                )

        except KeyboardInterrupt:
            print("[MONITOR] Stopped.")
            break
        except Exception as e:
            print(f"[MONITOR ERROR] {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()