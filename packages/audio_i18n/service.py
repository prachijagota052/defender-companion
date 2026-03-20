import os
import time

from packages.core.db import fetch_unspoken_user_alerts, mark_user_alert_spoken
from .settings import load_settings
from .tts import speak_interruptible
from .i18n import build_speech_text

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FLAG_FILE = os.path.join(BASE_DIR, "speaking.flag")
DISMISS_FILE = os.path.join(BASE_DIR, "dismiss.flag")


def set_speaking(flag: bool):
    try:
        if flag:
            with open(FLAG_FILE, "w", encoding="utf-8") as f:
                f.write("speaking")
        else:
            if os.path.exists(FLAG_FILE):
                os.remove(FLAG_FILE)
    except Exception as e:
        print(f"[FLAG ERROR] {e}")


def is_dismissed() -> bool:
    return os.path.exists(DISMISS_FILE)


def clear_dismiss():
    try:
        if os.path.exists(DISMISS_FILE):
            os.remove(DISMISS_FILE)
    except Exception as e:
        print(f"[DISMISS CLEAR ERROR] {e}")


def settings_signature(cfg):
    return (
        cfg.enabled,
        cfg.language,
        cfg.use_online_tts,
        cfg.rate_delta,
        cfg.voice_hint,
        cfg.max_steps_spoken,
    )


def build_quick_alert(alert, lang: str) -> str:
    threat = alert.threat_name or "Unknown Threat"

    if lang == "hi":
        return f"सुरक्षा चेतावनी। खतरा पाया गया। {threat}."
    if lang == "mr":
        return f"सुरक्षा इशारा. धोका आढळला. {threat}."
    return f"Security alert. Threat detected. {threat}."


def run_audio_service():
    print("[AUDIO] Service started...")

    while True:
        alerts = fetch_unspoken_user_alerts(limit=1)

        if not alerts:
            set_speaking(False)
            clear_dismiss()
            time.sleep(0.3)
            continue

        alert = alerts[0]
        cfg = load_settings()

        if not cfg.enabled:
            set_speaking(False)
            time.sleep(0.3)
            continue

        start_sig = settings_signature(cfg)

        quick_text = build_quick_alert(alert, cfg.language)
        full_text = build_speech_text(alert, cfg.language, cfg.max_steps_spoken)

        def should_stop():
            latest = load_settings()
            return is_dismissed() or settings_signature(latest) != start_sig

        print(f"[AUDIO] Quick alert for id={alert.id} in {cfg.language}")
        set_speaking(True)

        quick_finished = speak_interruptible(
            text=quick_text,
            lang=cfg.language,
            enabled=cfg.enabled,
            stop_checker=should_stop,
        )

        if is_dismissed():
            set_speaking(False)
            mark_user_alert_spoken(alert.id)
            clear_dismiss()
            print(f"[AUDIO] Alert {alert.id} dismissed during quick alert")
            time.sleep(0.2)
            continue

        if not quick_finished:
            set_speaking(False)
            time.sleep(0.2)
            continue

        latest_cfg = load_settings()
        if settings_signature(latest_cfg) != start_sig or not latest_cfg.enabled:
            set_speaking(False)
            time.sleep(0.2)
            continue

        print(f"[AUDIO] Full alert for id={alert.id} in {cfg.language}")

        full_finished = speak_interruptible(
            text=full_text,
            lang=cfg.language,
            enabled=cfg.enabled,
            stop_checker=should_stop,
        )

        set_speaking(False)

        if is_dismissed():
            mark_user_alert_spoken(alert.id)
            clear_dismiss()
            print(f"[AUDIO] Alert {alert.id} dismissed during full alert")
            time.sleep(0.2)
            continue

        latest_cfg = load_settings()

        if full_finished and latest_cfg.enabled and latest_cfg.language == cfg.language:
            mark_user_alert_spoken(alert.id)
            print(f"[AUDIO] Alert {alert.id} marked spoken")
        else:
            print(f"[AUDIO] Alert {alert.id} will retry with updated settings")

        time.sleep(0.2)


if __name__ == "__main__":
    try:
        run_audio_service()
    except KeyboardInterrupt:
        set_speaking(False)
        clear_dismiss()
        print("\n[AUDIO] Stopped.")