# src/viz.py

import matplotlib.pyplot as plt
import numpy as np

from .emotion_model import EMOTIONS, EMOTION_COLORS, blend_color, apply_style_to_color


def create_radar_chart(emotion_scores):
    """Create a radar chart of the dream's emotional structure."""
    values = [emotion_scores[e] for e in EMOTIONS]
    values.append(values[0])  # close the loop

    angles = np.linspace(0, 2 * np.pi, len(EMOTIONS), endpoint=False).tolist()
    angles.append(angles[0])

    fig, ax = plt.subplots(figsize=(4, 4), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(EMOTIONS)
    ax.set_yticklabels([])
    ax.set_title("Dream Emotion Radar", pad=20)
    fig.tight_layout()
    return fig


def create_aura_bar(emotion_scores, style: str):
    """
    Create a horizontal aura spectrum bar based on emotional strengths.
    """
    num_steps = 300
    colors = []

    for i in range(num_steps):
        t = i / (num_steps - 1)
        idx = int(t * (len(EMOTIONS) - 1))
        frac = t * (len(EMOTIONS) - 1) - idx

        emo1 = EMOTIONS[idx]
        emo2 = EMOTIONS[min(idx + 1, len(EMOTIONS) - 1)]
        c1 = EMOTION_COLORS[emo1]
        c2 = EMOTION_COLORS[emo2]

        base = blend_color(c1, c2, frac)
        strength = (emotion_scores[emo1] + emotion_scores[emo2]) / 2
        mixed = blend_color((0.0, 0.0, 0.0), base, 0.4 + 0.6 * strength)
        styled = apply_style_to_color(mixed, style)
        colors.append(styled)

    gradient = np.array(colors)[np.newaxis, :, :]

    fig, ax = plt.subplots(figsize=(6, 1.0))
    ax.imshow(gradient, aspect="auto")
    ax.set_axis_off()
    ax.set_title("Aura Energy Spectrum", pad=8)
    fig.tight_layout()
    return fig
