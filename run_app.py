import subprocess
import sys
import time
import os

# Get the absolute path of the folder where run_app.py lives
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

def start_companion():
    # We use 'cwd=ROOT_DIR' to ensure every process looks at the same 'data' folder
    p_listener = subprocess.Popen([sys.executable, "-m", "packages.logic.defender_monitor"], cwd=ROOT_DIR)
    p_runner = subprocess.Popen([sys.executable, "-m", "packages.logic.runner"], cwd=ROOT_DIR)
    p_audio = subprocess.Popen([sys.executable, "-m", "packages.audio_i18n.service"], cwd=ROOT_DIR)
    
    # ... rest of your run_app.py code ...

    print("\n✅ All systems active! Monitoring in the background.")
    print("💡 To test: Change a Windows Security setting or create an EICAR file.")
    print("🛑 Press Ctrl+C to shut down all services.")

    try:
        # Keep the main script alive while background processes run
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Shutting down services...")
        p_listener.terminate()
        p_runner.terminate()
        p_audio.terminate()
        print("👋 Goodbye!")

if __name__ == "__main__":
    start_companion()