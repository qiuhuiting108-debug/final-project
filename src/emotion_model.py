"""
emotion_model.py

Simple rule-based emotion model used as a fallback when
the OpenAI API is not available or fails.

It outputs a dictionary in the same structure as the
OpenAI-based analyzer so that the rest of the app can
use a unified interface.
"""

from collections import Counter
import re


def rule_based_emotion_model(dream_text: str):
    """
    Keyword-based emotion model.

    Different dream texts should produce different emotion patterns.

    Returns:
        {
          "symbolic_summary": str,
          "emotions": {
            "Fear": float,
            "Desire": float,
            "Calm": float,
            "Mystery": float,
            "Connection": float,
            "Transformation": float
          },
          "tarot_shadow": str,
          "tarot_energy": str,
          "tarot_guidance": str
        }
    """
    text_lower = dream_text.lower()
    words = re.findall(r"[a-z]+", text_lower)
    counts = Counter(words)

    def has_any(cands):
        return any(w in counts for w in cands)

    # base values
    emotions = {
        "Fear": 0.1,
        "Desire": 0.1,
        "Calm": 0.1,
        "Mystery": 0.1,
        "Connection": 0.1,
        "Transformation": 0.1,
    }

    # Fear related
    fear_words = [
        "afraid", "scared", "fear", "terrified", "nightmare",
        "dark", "shadow", "monster", "chasing", "chase",
        "run", "running", "falling", "lost"
    ]
    if has_any(fear_words):
        emotions["Fear"] += 0.5

    if "tunnel" in counts or "underground" in counts:
        emotions["Fear"] += 0.2
        emotions["Mystery"] += 0.2

    if "exam" in counts or "test" in counts:
        emotions["Fear"] += 0.3
        emotions["Desire"] += 0.2

    # Desire / longing
    desire_words = [
        "love", "loved", "kiss", "want", "wish",
        "longing", "desire", "romantic", "date"
    ]
    if has_any(desire_words):
        emotions["Desire"] += 0.5

    # Calm / safe
    calm_words = ["floating", "fly", "flying", "calm", "quiet", "peaceful"]
    water_words = ["sea", "ocean", "water", "lake", "river", "waves"]
    if has_any(calm_words) or has_any(water_words):
        emotions["Calm"] += 0.5
        emotions["Mystery"] += 0.1

    # Mystery
    mystery_words = [
        "strange", "weird", "unknown", "portal", "door",
        "fog", "smoke", "mysterious", "secret"
    ]
    if has_any(mystery_words):
        emotions["Mystery"] += 0.5

    # Connection
    connection_words = [
        "family", "friend", "friends", "together",
        "group", "people", "crowd", "someone"
    ]
    if has_any(connection_words):
        emotions["Connection"] += 0.5

    # Transformation / change
    transform_words = [
        "change", "changed", "transform", "transformation",
        "reborn", "rebirth", "door", "gate", "opening",
        "melting", "reforming", "new"
    ]
    if has_any(transform_words):
        emotions["Transformation"] += 0.5

    # normalize to [0, 1]
    max_v = max(emotions.values()) or 1.0
    for k in emotions:
        emotions[k] = min(1.0, emotions[k] / max_v)

    symbolic_summary = (
        "This is a rule-based interpretation that detects words related to fear, "
        "desire, calm, mystery, connection, and transformation in your dream "
        "and converts them into emotional intensities."
    )
    tarot_shadow = (
        "Your subconscious is processing these mixed feelings and turning them "
        "into symbolic images during sleep."
    )
    tarot_energy = (
        "The aura around this dream is a blend of your current emotional state "
        "and hidden wishes."
    )
    tarot_guidance = (
        "Notice which part of the dream felt the strongest. That emotional color "
        "is pointing toward something important in your waking life."
    )

    return {
        "symbolic_summary": symbolic_summary,
        "emotions": emotions,
        "tarot_shadow": tarot_shadow,
        "tarot_energy": tarot_energy,
        "tarot_guidance": tarot_guidance,
    }
