import os
import subprocess
import sys
import time

from packages.core.db import init_db, mark_all_shown_alerts_spoken

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SPEAKING_FILE = os.path.join(ROOT_DIR, "speaking.flag")
DISMISS_FILE = os.path.join(ROOT_DIR, "dismiss.flag")


def cleanup_runtime_flags():
    for path in (SPEAKING_FILE, DISMISS_FILE):
        try:
            if os.path.exists(path):
                os.remove(path)
        except Exception as e:
            print(f"[RUN_APP CLEANUP ERROR] {path} | {e}")


def start_companion():
    init_db()
    cleanup_runtime_flags()
    mark_all_shown_alerts_spoken()

    processes = []
    commands = [
        [sys.executable, "-m", "packages.logic.defender_monitor"],
        [sys.executable, "-m", "packages.logic.runner"],
        [sys.executable, "-m", "packages.audio_i18n.service"],
        [sys.executable, "-m", "packages.ui.main"],
    ]

    for cmd in commands:
        p = subprocess.Popen(cmd, cwd=ROOT_DIR)
        processes.append(p)

    print("\n✅ Defender Companion is running.")
    print("It will monitor continuously and only alert when a threat is detected.")
    print("🛑 Press Ctrl+C to stop all services.")

    try:
        while True:
            dead = [p for p in processes if p.poll() is not None]
            if dead:
                print("\n[RUN_APP] One or more services exited unexpectedly:")
                for p in dead:
                    print(f"  PID {p.pid} exit code = {p.poll()}")
                break
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
    finally:
        for p in processes:
            if p.poll() is None:
                p.terminate()
        cleanup_runtime_flags()
        print("👋 Goodbye!")


if __name__ == "__main__":
    start_companion()