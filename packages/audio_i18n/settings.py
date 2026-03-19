import json
from pathlib import Path
from dataclasses import dataclass
from typing import Optional

# Path to the JSON file in the same directory
SETTINGS_PATH = Path(__file__).resolve().parent / "settings.json"

@dataclass
class AudioSettings:
    enabled: bool
    language: str
    use_online_tts: bool
    rate_delta: int
    voice_hint: Optional[str]
    max_steps_spoken: int

DEFAULT_DICT = {
    "enabled": True,
    "language": "en",
    "use_online_tts": True,
    "rate_delta": 0,
    "voice_hint": "",
    "max_steps_spoken": 2
}

def load_settings() -> AudioSettings:
    """Loads settings from JSON. Creates default JSON if missing."""
    if not SETTINGS_PATH.exists():
        with open(SETTINGS_PATH, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_DICT, f, indent=2)
        print(f"--- Created default settings.json at {SETTINGS_PATH} ---")
        data = DEFAULT_DICT
    else:
        try:
            with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = DEFAULT_DICT

    return AudioSettings(
        enabled=data.get("enabled", True),
        language=data.get("language", "en"),
        use_online_tts=data.get("use_online_tts", True),
        rate_delta=data.get("rate_delta", 0),
        voice_hint=data.get("voice_hint", ""),
        max_steps_spoken=data.get("max_steps_spoken", 2)
    )
