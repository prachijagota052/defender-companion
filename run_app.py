import os
import subprocess
import sys
import time

from packages.core.db import init_db

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


def start_companion():
    init_db()

    processes = []

    commands = [
        [sys.executable, "-m", "packages.logic.defender_monitor"],
        [sys.executable, "-m", "packages.logic.runner"],
        [sys.executable, "-m", "packages.audio_i18n.service"],
        [sys.executable, "-m", "packages.ui.main"],
    ]

    for cmd in commands:
        processes.append(subprocess.Popen(cmd, cwd=ROOT_DIR))

    print("\n✅ Defender Companion is running in background.")
    print("It will monitor continuously and only alert when a threat is detected.")
    print("🛑 Press Ctrl+C to stop all services.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down services...")
        for p in processes:
            p.terminate()
        print("👋 Goodbye!")


if __name__ == "__main__":
    start_companion()