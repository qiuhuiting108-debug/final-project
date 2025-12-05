"""
viz.py

Visualization utilities:
- Radar chart for the 6D emotion model.
- Aura energy spectrum bar.
"""

from math import pi
from typing import Dict

import matplotlib.pyplot as plt


def plot_emotion_radar(emotions: Dict[str, float]):
    """
    Plot a 6-axis radar chart for the emotional values.
    """
    labels = list(emotions.keys())
    num_vars = len(labels)
    values = list(emotions.values())
    values += values[:1]  # close polygon

    angles = [n / float(num_vars) * 2 * pi for n in range(num_vars)]
    angles += angles[:1]

    fig, ax = plt.subplots(subplot_kw=dict(polar=True))
    fig.set_size_inches(4, 4)

    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_yticklabels([])

    ax.set_title("Dream Emotion Radar", pad=20)
    return fig


def plot_aura_bar(emotions: Dict[str, float]):
    """
    Plot a horizontal bar showing the aura energy distribution
    according to the 6 emotional dimensions.
    """
    fig, ax = plt.subplots(figsize=(4, 1))

    color_map = {
        "Fear": "#1f3b73",          # deep blue
        "Desire": "#e75480",        # pink-red
        "Calm": "#7fc8f8",          # soft blue
        "Mystery": "#6a4c93",       # violet
        "Connection": "#f4a261",    # warm orange
        "Transformation": "#f6e05e" # golden yellow
    }

    total = sum(emotions.values()) + 1e-6
    start = 0.0
    for name, value in emotions.items():
        width = value / total
        ax.barh(0, width, left=start, color=color_map.get(name, "#888888"))
        start += width

    ax.set_xlim(0, 1)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_title("Aura Energy Spectrum")

    return fig
