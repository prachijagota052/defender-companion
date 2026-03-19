import json
from pathlib import Path
from typing import Dict

_LOCALES_DIR = Path(__file__).resolve().parent / "locales"


def _load(lang: str) -> Dict[str, str]:
    path = _LOCALES_DIR / f"{lang}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def t(key: str, lang: str = "en") -> str:
    """Translate key in selected language. Fallback: selected lang -> English -> key."""
    lang_map = _load(lang)
    if key in lang_map:
        return lang_map[key]

    en_map = _load("en")
    return en_map.get(key, key)