import win32evtlog
import xml.etree.ElementTree as ET
import json
import time
from datetime import datetime
from packages.core.db import insert_threat_alert
from packages.core.models import ThreatAlert

LOG_PATH = "Microsoft-Windows-Windows Defender/Operational"

def extract_event_data(root, ns):
    event_data = root.find("ns:EventData", ns)
    data_dict = {}
    if event_data is not None:
        for data in event_data.findall("ns:Data", ns):
            name = data.attrib.get("Name")
            data_dict[name] = data.text
    return data_dict

def callback(action, context, event):
    if action == win32evtlog.EvtSubscribeActionDeliver:
        try:
            xml_data = win32evtlog.EvtRender(event, win32evtlog.EvtRenderEventXml)
            root = ET.fromstring(xml_data)
            ns = {"ns": "http://schemas.microsoft.com/win/2004/08/events/event"}
            event_id = root.find("ns:System/ns:EventID", ns).text
            
            # 1116=Detection, 5007=Config Change (Seen in your Event Viewer)
            if event_id in ["1116", "1117", "5007"]:
                data = extract_event_data(root, ns)
                t_name = data.get("Threat Name") if event_id != "5007" else "Security Setting Changed"
                
                new_alert = ThreatAlert(
                    timestamp=datetime.now(),
                    source_type="Antivirus",
                    file_path=data.get("Path", "System Settings"),
                    threat_name=t_name,
                    action_taken="Logged",
                    severity="Informational" if event_id == "5007" else "High",
                    raw_message=json.dumps(data) 
                )
                insert_threat_alert(new_alert)
                print(f"🛡️ Defender Event {event_id} captured and saved to DB.")
        except Exception as e:
            print(f"❌ Listener Error: {e}")

if __name__ == "__main__":
    subscription = win32evtlog.EvtSubscribe(LOG_PATH, win32evtlog.EvtSubscribeToFutureEvents, None, callback)
    while True: time.sleep(1)