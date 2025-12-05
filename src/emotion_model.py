"""
emotion_model.py

Simple rule-based emotion model used as a fallback when
the OpenAI API is not available or fails.

It outputs a dictionary in the same structure as the
OpenAI-based analyzer so that the rest of the app can
use a unified interface.
"""

def rule_based_emotion_model(dream_text: str):
    """
    Very simple keyword-based emotion model.

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

    emotions = {
        "Fear": 0.2,
        "Desire": 0.2,
        "Calm": 0.2,
        "Mystery": 0.2,
        "Connection": 0.2,
        "Transformation": 0.2,
    }

    def boost(name, value):
        emotions[name] = emotions.get(name, 0.0) + value

    # Simple keyword lists (can be extended)
    fear_words = [
        "chase", "chasing", "afraid", "scared", "dark",
        "monster", "run away", "fall", "falling", "exam", "test"
    ]
    desire_words = [
        "kiss", "love", "want", "wish", "date",
        "beautiful", "pretty", "wedding"
    ]
    calm_words = [
        "sea", "ocean", "beach", "floating", "fly",
        "flying", "sky", "calm", "peaceful"
    ]
    mystery_words = [
        "fog", "unknown", "strange", "mystery",
        "mysterious", "shadow", "portal"
    ]
    connection_words = [
        "family", "friend", "friends", "together",
        "hug", "group", "people"
    ]
    transform_words = [
        "change", "transform", "transformation",
        "reborn", "rebirth", "bridge", "door", "threshold"
    ]

    for w in fear_words:
        if w in text_lower:
            boost("Fear", 0.2)
    for w in desire_words:
        if w in text_lower:
            boost("Desire", 0.2)
    for w in calm_words:
        if w in text_lower:
            boost("Calm", 0.2)
    for w in mystery_words:
        if w in text_lower:
            boost("Mystery", 0.2)
    for w in connection_words:
        if w in text_lower:
            boost("Connection", 0.2)
    for w in transform_words:
        if w in text_lower:
            boost("Transformation", 0.2)

    # Small global adjustments
    if "exam" in text_lower or "test" in text_lower:
        boost("Fear", 0.1)
        boost("Desire", 0.1)
    if "water" in text_lower or "sea" in text_lower or "ocean" in text_lower:
        boost("Mystery", 0.1)
        boost("Calm", 0.05)

    # Clamp values to [0, 1]
    for k in emotions:
        emotions[k] = max(0.0, min(1.0, emotions[k]))

    symbolic_summary = (
        "This is a simplified, rule-based interpretation of your dream. "
        "The system looks for words related to fear, desire, calmness, "
        "mystery, connection, and transformation, and maps them into "
        "numerical emotional values."
    )
    tarot_shadow = (
        "Your subconscious is trying to work with these mixed emotions "
        "and unresolved questions."
    )
    tarot_energy = (
        "The aura energy here is a blend of tension, curiosity, "
        "and a wish for emotional change."
    )
    tarot_guidance = (
        "Take time to name how you feel in waking life, and move one small "
        "step toward what you truly want."
    )

    return {
        "symbolic_summary": symbolic_summary,
        "emotions": emotions,
        "tarot_shadow": tarot_shadow,
        "tarot_energy": tarot_energy,
        "tarot_guidance": tarot_guidance,
    }
