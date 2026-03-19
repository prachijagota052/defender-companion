import win32evtlog
import xml.etree.ElementTree as ET
import json
from datetime import datetime

# Import the tools your teammates built in the 'core' package
from packages.core.db import insert_threat_alert
from packages.core.models import ThreatAlert

LOG_PATH = "Microsoft-Windows-Windows Defender/Operational"

print("🛡️ Member 1: Real-Time Windows Defender Monitor Active...")
print("📡 Listening for threats and syncing to companion.db...\n")

# ----------------------------
# 1️⃣ Extract EventData from XML
# ----------------------------
def extract_event_data(root, ns):
    event_data = root.find("ns:EventData", ns)
    data_dict = {}
    if event_data is not None:
        for data in event_data.findall("ns:Data", ns):
            name = data.attrib.get("Name")
            value = data.text
            data_dict[name] = value
    return data_dict

# ----------------------------
# 2️⃣ Real-Time Callback Function
# ----------------------------
def callback(action, context, event):
    if action == win32evtlog.EvtSubscribeActionDeliver:
        try:
            xml_data = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
            root = ET.fromstring(xml_data)
            ns = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}

            # Get basic Info
            event_id = root.find("ns:System/ns:EventID", ns).text
            
            # We only care about Threat IDs (1116 = Detected, 1117 = Action Taken)
            if event_id in ["1116", "1117"]:
                data = extract_event_data(root, ns)
                
                # --- THE HANDOVER ---
                # We package the data into the ThreatAlert model
                new_alert = ThreatAlert(
                    timestamp=datetime.now(),
                    source_type="Antivirus",
                    file_path=data.get("Path"),
                    threat_name=data.get("Threat Name"),
                    action_taken=data.get("Action"),
                    severity=data.get("Severity"),
                    raw_message=json.dumps(data) 
                )

                # Send it to the Database (processed will be 0 by default)
                alert_id = insert_threat_alert(new_alert)
                
                print(f"🚨 THREAT DETECTED: {new_alert.threat_name}")
                print(f"📦 Logged to DB (ID: {alert_id}) for Member 2 to process.\n")

        except Exception as e:
            print(f"❌ Error processing event: {e}")

# ----------------------------
# 3️⃣ Subscribe & Run
# ----------------------------
subscription = win32evtlog.EvtSubscribe(
    LOG_PATH,
    win32evtlog.EvtSubscribeToFutureEvents,
    None,
    callback
)

try:
    while True:
        import time
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Monitoring stopped.")