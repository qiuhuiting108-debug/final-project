# src/emotion_model.py

import numpy as np

# Global emotion dimensions (order matters in plots)
EMOTIONS = ["Fear", "Desire", "Calm", "Mystery", "Connection", "Transformation"]

# Base RGB colors (0–1) for each emotion
EMOTION_COLORS = {
    "Fear": (0.1, 0.1, 0.4),           # deep blue / indigo
    "Desire": (0.9, 0.3, 0.3),         # warm red / pink
    "Calm": (0.3, 0.7, 0.6),           # soft green / blue
    "Mystery": (0.4, 0.2, 0.5),        # violet / twilight
    "Connection": (1.0, 0.6, 0.2),     # warm orange / peach
    "Transformation": (1.0, 0.9, 0.5), # gold / white light
}

# Keyword → emotion weight mapping (Layer 2)
KEYWORD_EMOTION_WEIGHTS = {
    "water": {"Calm": 0.4, "Fear": 0.2, "Mystery": 0.2},
    "sea": {"Calm": 0.5, "Mystery": 0.2},
    "ocean": {"Calm": 0.4, "Mystery": 0.3},
    "river": {"Calm": 0.4, "Connection": 0.2},
    "drown": {"Fear": 0.6, "Mystery": 0.2},
    "fire": {"Desire": 0.4, "Transformation": 0.3},
    "bridge": {"Transformation": 0.4, "Connection": 0.3},
    "fall": {"Fear": 0.6, "Transformation": 0.2},
    "train": {"Mystery": 0.3, "Connection": 0.2, "Fear": 0.2},
    "station": {"Mystery": 0.3, "Connection": 0.3},
    "stranger": {"Mystery": 0.4, "Connection": 0.2},
    "dark": {"Fear": 0.5, "Mystery": 0.3},
    "light": {"Transformation": 0.4, "Calm": 0.3},
    "white dress": {"Desire": 0.2, "Transformation": 0.4, "Calm": 0.2},
    "door": {"Transformation": 0.4, "Mystery": 0.2},
    "corridor": {"Mystery": 0.4, "Fear": 0.2},
    "chase": {"Fear": 0.6, "Desire": 0.2},
    "exam": {"Fear": 0.5, "Desire": 0.3},
    "family": {"Connection": 0.6, "Calm": 0.2},
    "friend": {"Connection": 0.6, "Calm": 0.2},
    "lover": {"Desire": 0.5, "Connection": 0.3},
    "kiss": {"Desire": 0.5, "Connection": 0.3},
    "argue": {"Fear": 0.4, "Connection": -0.2},
    "fight": {"Fear": 0.5, "Connection": -0.3},
    "death": {"Fear": 0.7, "Transformation": 0.3},
    "reborn": {"Transformation": 0.6, "Calm": 0.2},
    "flying": {"Desire": 0.3, "Transformation": 0.4, "Calm": 0.3},
    "school": {"Fear": 0.2, "Desire": 0.2, "Connection": 0.1},
}


def blend_color(c1, c2, alpha: float = 0.5):
    """Linear blend between two RGB colors."""
    return tuple((1 - alpha) * a + alpha * b for a, b in zip(c1, c2))


def apply_style_to_color(color, style: str):
    """Adapt a base color to the selected aura style."""
    r, g, b = color

    if style == "Pastel":
        # Move toward white, softer look
        return blend_color((r, g, b), (1.0, 1.0, 1.0), 0.5)

    if style == "Cyber":
        # Higher contrast, neon-like
        return (min(r * 1.3, 1.0), min(g * 1.3, 1.0), min(b * 1.5, 1.0))

    if style == "Golden":
        gold = (1.0, 0.84, 0.3)
        return blend_color((r, g, b), gold, 0.6)

    if style == "Mystic":
        mystic = (0.3, 0.2, 0.5)
        return blend_color((r, g, b), mystic, 0.5)

    return color


def extract_emotions(text: str):
    """
    Convert dream text into six emotional factors (0–1).
    Simple keyword-based heuristic model.
    """
    text_lower = text.lower()
    scores = {e: 0.1 for e in EMOTIONS}  # small base score

    for keyword, weights in KEYWORD_EMOTION_WEIGHTS.items():
        if keyword in text_lower:
            for emo, weight in weights.items():
                if emo in scores:
                    scores[emo] += weight

    values = np.array(list(scores.values()), dtype=float)
    max_v = float(values.max())
    min_v = float(values.min())

    if max_v == min_v:
        # Fallback profile if no signal is found
        return {
            "Fear": 0.25,
            "Desire": 0.45,
            "Calm": 0.6,
            "Mystery": 0.4,
            "Connection": 0.5,
            "Transformation": 0.5,
        }

    normalized = (values - min_v) / (max_v - min_v)
    return {emo: float(v) for emo, v in zip(EMOTIONS, normalized)}
