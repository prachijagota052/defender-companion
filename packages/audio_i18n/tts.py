from typing import Optional
import pyttsx3


def speak(text: str, enabled: bool = True, rate_delta: int = 0, voice_hint: Optional[str] = None) -> None:
    """
    Offline TTS using pyttsx3.
    enabled: if False, do nothing.
    rate_delta: adjusts speaking rate (+/-). 0 is default.
    voice_hint: substring to match a voice name (best effort).
    """
    if not enabled or not text.strip():
        return

    engine = pyttsx3.init()

    # Rate
    try:
        base_rate = engine.getProperty("rate")
        engine.setProperty("rate", base_rate + rate_delta)
    except Exception:
        pass

    # Voice selection (best effort)
    if voice_hint:
        try:
            voices = engine.getProperty("voices")
            for v in voices:
                if voice_hint.lower() in v.name.lower():
                    engine.setProperty("voice", v.id)
                    break
        except Exception:
            pass

    engine.say(text)
    engine.runAndWait()