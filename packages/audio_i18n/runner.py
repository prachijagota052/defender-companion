from typing import Optional

from packages.core.db import fetch_unspoken_user_alerts, mark_user_alert_spoken
from .i18n import t
from .tts import speak


def build_speech(alert, lang: str) -> str:
    title = alert.title or t("title_default", lang)
    why = alert.why_blocked or t("why_default", lang)
    explain = alert.explanation or t("explain_default", lang)

    parts = [
        t("speak_prefix", lang),
        title,
        why,
        explain,
    ]

    # Keep audio short (2 steps max)
    if alert.recommended_steps:
        steps = alert.recommended_steps[:2]
        parts.append(t("steps_prefix", lang) + " " + " ".join(steps))

    return " ".join(parts)


def main(lang: str = "en", enabled: bool = True, rate_delta: int = 0, voice_hint: Optional[str] = None) -> None:
    alerts = fetch_unspoken_user_alerts(limit=10)

    if not alerts:
        print("No new alerts to speak.")
        return

    for a in alerts:
        text = build_speech(a, lang)
        print(f"Speaking id={a.id} | {a.title} | {a.severity}")
        speak(text, enabled=enabled, rate_delta=rate_delta, voice_hint=voice_hint)
        mark_user_alert_spoken(a.id)
        print(f"Marked spoken id={a.id}")


if __name__ == "__main__":
    # Change lang to "hi" or "mr" for testing
    main(lang="en", enabled=True, rate_delta=0)