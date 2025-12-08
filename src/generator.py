# src/generator.py

import matplotlib.pyplot as plt
import numpy as np

from .emotion_model import EMOTIONS, EMOTION_COLORS, blend_color, apply_style_to_color


def create_aura_poster(emotion_scores, style: str):
    """
    Create the generative Aura Art Poster.
    Emotion values influence color, size, and layering of blobs.
    """
    fig, ax = plt.subplots(figsize=(5, 7))

    # Background depends on style
    if style in ["Mystic", "Cyber"]:
        ax.set_facecolor("#05050a")
    else:
        ax.set_facecolor("#f8f5ff")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    base_blobs = 18
    total_activation = float(sum(emotion_scores.values()))
    n_blobs = base_blobs + int(total_activation * 8)

    rng = np.random.default_rng(42)  # deterministic for grading

    for _ in range(n_blobs):
        # Choose an emotion according to its probability
        probs = np.array([emotion_scores[e] for e in EMOTIONS], dtype=float)
        probs = probs / probs.sum()
        emo_index = int(rng.choice(len(EMOTIONS), p=probs))
        emo = EMOTIONS[emo_index]

        base_color = EMOTION_COLORS[emo]
        color = apply_style_to_color(base_color, style)

        # Position
        x = float(rng.uniform(0.1, 0.9))
        y = float(rng.uniform(0.1, 0.9))

        # Size depends on intensity
        intensity = float(emotion_scores[emo])
        radius = 0.08 + intensity * float(rng.uniform(0.03, 0.15))

        # Alpha depends on style and intensity
        if style == "Cyber":
            alpha = 0.45 + intensity * 0.3
        elif style == "Mystic":
            alpha = 0.35 + intensity * 0.35
        elif style == "Golden":
            alpha = 0.4 + intensity * 0.3
        else:  # Pastel / default
            alpha = 0.3 + intensity * 0.25

        # Main blob
        ellipse = plt.Circle((x, y), radius, color=color, alpha=alpha)
        ax.add_patch(ellipse)

        # Soft glow
        glow_radius = radius * 1.6
        if style == "Pastel":
            glow_color = blend_color(color, (1, 1, 1), 0.7)
        else:
            glow_color = color
        glow_alpha = alpha * 0.35
        glow = plt.Circle((x, y), glow_radius, color=glow_color, alpha=glow_alpha)
        ax.add_patch(glow)

    ax.set_title("Aura Tarot Dream Poster", fontsize=14, pad=18)
    fig.tight_layout()
    return fig
