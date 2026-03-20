import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Optional

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
    if not SETTINGS_PATH.exists():
        SETTINGS_PATH.write_text(json.dumps(DEFAULT_DICT, indent=2), encoding="utf-8")
        data = DEFAULT_DICT
    else:
        try:
            data = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        except Exception:
            data = DEFAULT_DICT

    return AudioSettings(
        enabled=data.get("enabled", True),
        language=data.get("language", "en"),
        use_online_tts=data.get("use_online_tts", True),
        rate_delta=data.get("rate_delta", 0),
        voice_hint=data.get("voice_hint", ""),
        max_steps_spoken=data.get("max_steps_spoken", 2),
    )


def save_settings(settings: AudioSettings) -> None:
    SETTINGS_PATH.write_text(
        json.dumps(asdict(settings), indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def config_signature(settings: AudioSettings) -> tuple:
    return (
        settings.enabled,
        settings.language,
        settings.use_online_tts,
        settings.rate_delta,
        settings.voice_hint,
        settings.max_steps_spoken,
    )