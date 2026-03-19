import time
from packages.core.db import fetch_unspoken_user_alerts, mark_user_alert_spoken
from .i18n import t
from .tts import speak
from .settings import load_settings  # This ensures we get the latest lang/mode

def build_speech(alert, lang: str) -> str:
    """Your original logic, kept exactly as you wrote it."""
    title = alert.title or t("title_default", lang)
    why = alert.why_blocked or t("why_default", lang)
    explain = alert.explanation or t("explain_default", lang)

    parts = [
        t("speak_prefix", lang),
        title,
        why,
        explain,
    ]

    if alert.recommended_steps:
        steps = alert.recommended_steps[:2]
        parts.append(t("steps_prefix", lang) + " " + " ".join(steps))

    return " ".join(parts)

def run_audio_service():
    print("--- Defender Companion Audio Service is Running ---")
    print("Polling for new alerts... (Ctrl+C to stop)")

    while True:
        # 1. Always load settings at the start of the loop
        # This allows the UI to change language or mute audio instantly!
        cfg = load_settings()

        if not cfg.enabled:
            time.sleep(2)
            continue

        # 2. Get one alert at a time to keep it real-time
        alerts = fetch_unspoken_user_alerts(limit=1)

        for a in alerts:
            # 3. Use the language from settings.json
            text = build_speech(a, cfg.language)
            
            print(f"[{cfg.language.upper()}] Speaking ID: {a.id} - {a.title}")
            
            # 4. Speak using the Online/Offline logic we built in tts.py
            # Note: Ensure your tts.py 'speak' function accepts 'use_online'
            speak(text, lang=cfg.language, use_online=cfg.use_online_tts)
            
            # 5. Mark as spoken so it doesn't repeat
            mark_user_alert_spoken(a.id)
            print(f"Success: Alert {a.id} marked as spoken.")

        # 6. Wait a few seconds before checking the DB again
        time.sleep(3)

if __name__ == "__main__":
    try:
        run_audio_service()
    except KeyboardInterrupt:
        print("\nAudio service shut down gracefully.")
