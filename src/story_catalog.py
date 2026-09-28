"""
Multiverso Comic - Story Catalog
Assigns Google Gemini 3.8 TTS voice 'Puck' and metadata to all comic stories.
"""

from typing import Optional
from .editorial_catalog import EDITORIAL_STORIES

# Default Voice Configuration (Gemini 3.8 Puck Standard)
DEFAULT_VOICE = "Puck"
DEFAULT_TTS_MODEL = "gemini-3.8-flash-tts"
DEFAULT_FALLBACK_TTS_MODEL = "gemini-3.8-flash-lite-tts"
VOICE_STYLE_DIRECTION = "Narrador de cómic con ritmo rápido, apasionado, tenso y enérgico en español latinoamericano"

# Attach voice configuration to every story
STORY_CATALOG = []
for _story in EDITORIAL_STORIES:
    _s = dict(_story)
    _s.setdefault("voice", DEFAULT_VOICE)
    _s.setdefault("tts_model", DEFAULT_TTS_MODEL)
    _s.setdefault("fallback_tts_model", DEFAULT_FALLBACK_TTS_MODEL)
    _s.setdefault("style_direction", VOICE_STYLE_DIRECTION)
    STORY_CATALOG.append(_s)


def get_all_stories() -> list[dict]:
    """Retorna todas las historias editoriales con la configuración de voz Puck."""
    return STORY_CATALOG


def get_story_by_id(story_id: str) -> Optional[dict]:
    """Busca una historia específica por su ID."""
    for s in STORY_CATALOG:
        if s.get("id") == story_id:
            return s
    return None


def get_unproduced_stories(ledger: list[dict]) -> list[dict]:
    """Retorna las historias disponibles que aún no han sido producidas."""
    from .cloud_runner import is_duplicate
    return [s for s in STORY_CATALOG if not is_duplicate(s, ledger)[0]]
