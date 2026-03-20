import subprocess
import sys
import time
import os
# Import your DB functions
from packages.core.db import (
    fetch_unprocessed_threat_alerts, 
    mark_threat_processed, 
    insert_user_alert
)
from packages.logic.engine import convert_to_user_alert

def run_logic_engine():
    print("🧠 Logic Engine (Runner) is active and polling for threats...")
    
    while True:
        try:
            # 1. Check for new raw threats from the Listener
            threats = fetch_unprocessed_threat_alerts(limit=1)
            
            if threats:
                threat = threats[0]
                print(f"🚨 New threat found: {threat.threat_name}. Processing...")

                # 2. Convert raw threat to Detailed UserAlert
                user_alert = convert_to_user_alert(threat)
                
                # 3. Save to user_alerts table (this wakes up the Audio Service)
                insert_user_alert(user_alert)
                
                # 4. Mark the raw threat as done
                mark_threat_processed(threat.id)
                print(f"✅ Threat {threat.id} processed. Triggering UI Pop-up...")

                # 5. LAUNCH THE UI POP-UP
                # We use the current python executable to run the UI module
                subprocess.Popen([sys.executable, "-m", "packages.ui.main"])
            
        except Exception as e:
            print(f"❌ Runner Error: {e}")
        
        # Poll every 2 seconds
        time.sleep(2)

if __name__ == "__main__":
    try:
        run_logic_engine()
    except KeyboardInterrupt:
        print("\nStopping Runner...")