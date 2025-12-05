"""
generator.py

Generative abstract poster engine for the
Aura Tarot Dream Analyzer.

This version focuses on:
- Rich color gradients (colormaps)
- Aura / ripple / energy field feeling
- Very light geometric accents (optional)

Styles:
    "Aura Focus"       -> almost pure aura / energy field
    "Hybrid"           -> aura + a few soft rectangles
    "Geometric Focus"  -> aura + slightly stronger geometry
"""

from typing import Dict
import random

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Helper: choose colormap based on emotions
# ---------------------------------------------------------------------


def choose_cmap(emotions: Dict[str, float]) -> str:
    """
    Map the 6D emotion vector to a matplotlib colormap.
    This is where "mood -> color style" happens.
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    # Sum for normalization
    s = fear + desire + calm + mystery + connection + transform + 1e-6

    fear_n = fear / s
    desire_n = desire / s
    calm_n = calm / s
    mystery_n = mystery / s

    # Simple rule:
    # - Fear + mystery  -> darker / mystical maps
    # - Desire + connection -> warm maps
    # - Calm high -> cool, clean maps
    if fear_n + mystery_n > 0.5:
        return "twilight"
    elif desire_n + connection > 0.5:
        return "plasma"
    elif calm_n > 0.4:
        return "viridis"
    else:
        # Mixed state
        return "magma"


# ---------------------------------------------------------------------
# Aura / field generation
# ---------------------------------------------------------------------


def generate_aura_field(emotions: Dict[str, float], resolution: int = 600):
    """
    Create a 2D scalar field that feels like an energy / aura pattern.
    We only return the scalar field; colormap is applied later.
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    x = np.linspace(-1.6, 1.6, resolution)
    y = np.linspace(-1.6, 1.6, resolution)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)

    # Base radial glow: calm makes it softer / wider,
    # fear makes it sharper and more concentrated.
    base = np.exp(-R**2 * (1.5 + 1.5 * fear - 0.8 * calm))

    # Off-center "cores" driven by desire / connection
    core1 = np.exp(-((X - 0.45)**2 + (Y + 0.1)**2) * (4 + 2 * desire))
    core2 = np.exp(-((X + 0.35)**2 + (Y - 0.2)**2) * (4 + 2 * connection))

    # Ring-like structures from transformation
    rings = np.cos(8 * R - 3 * transform) * np.exp(-R**2 * 2.0)

    # Angular (theta) waves for mystery
    angular_waves = np.sin(5 * theta + 4 * R) * np.exp(-R**2 * 1.3)

    field = (
        0.9 * base
        + 0.6 * desire * core1
        + 0.6 * connection * core2
        + 0.4 * transform * rings
        + 0.4 * mystery * angular_waves
    )

    # Small global bump if emotions are all low – avoid flat image
    total_emotion = fear + desire + calm + mystery + connection + transform
    if total_emotion < 0.6:
        field += 0.2 * np.exp(-R**2 * 1.2)

    # Normalize field to 0–1
    field = field - field.min()
    field = field / (field.max() + 1e-6)
    return field


def draw_aura_layer(ax, emotions: Dict[str, float], resolution: int = 600):
    """
    Draw the aura field using a colormap chosen by emotions.
    """
    cmap_name = choose_cmap(emotions)
    field = generate_aura_field(emotions, resolution=resolution)

    ax.imshow(
        field,
        cmap=cmap_name,
        extent=(0, 1, 0, 1),
        origin="lower",
    )

    return field  # in case we want to overlay rings etc. later


# ---------------------------------------------------------------------
# Geometric accents (very light)
# ---------------------------------------------------------------------


def draw_geometric_accents(ax, emotions: Dict[str, float], seed: int = 0, density_scale: float = 1.0):
    """
    Light geometric accents: a few semi-transparent rectangles.
    If you want almost no rectangles, use density_scale < 1.
    """
    random.seed(seed)
    np.random.seed(seed)

    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    transform = emotions["Transformation"]

    # Pastel-ish palette as accents (only a few used)
    palette = [
        (0.96, 0.74, 0.80),  # soft pink
        (0.80, 0.86, 0.97),  # light blue
        (0.88, 0.90, 0.78),  # gentle green
        (0.98, 0.88, 0.70),  # peach
        (0.86, 0.80, 0.92),  # lavender
    ]

    # Base number of shapes – not a grid now, but random placements
    base_n = int(6 * density_scale)
    extra_n = int(10 * transform * density_scale)
    n_shapes = base_n + extra_n

    for _ in range(n_shapes):
        # More calm -> more empty, so we skip with some probability
        if random.random() < 0.3 + 0.3 * calm:
            continue

        cx = random.uniform(0.1, 0.9)
        cy = random.uniform(0.1, 0.9)

        # Size based on fear / desire
        base_size = 0.08 + 0.12 * (fear + desire)
        w = base_size * random.uniform(0.7, 1.4)
        h = base_size * random.uniform(0.6, 1.4)

        alpha = 0.06 + 0.22 * (fear + desire)

        color = random.choice(palette)

        rect = plt.Rectangle(
            (cx - w / 2, cy - h / 2),
            w,
            h,
            linewidth=0,
            color=color,
            alpha=alpha,
        )
        ax.add_patch(rect)


# ---------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------


def generate_hybrid_poster(
    emotions: Dict[str, float],
    style: str = "Hybrid",
    seed: int = 0,
):
    """
    Main entry point used by the Streamlit app.

    style:
        "Aura Focus"       -> almost pure aura field
        "Hybrid"           -> aura + some geometric accents
        "Geometric Focus"  -> aura + more shapes (still not too many)
    """
    fig, ax = plt.subplots(figsize=(4.5, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Draw aura first
    field = draw_aura_layer(ax, emotions, resolution=640)

    # Adjust aura visibility by style
    if style == "Geometric Focus":
        for im in ax.images:
            im.set_alpha(0.80)
        draw_geometric_accents(ax, emotions, seed=seed, density_scale=1.4)
    elif style == "Aura Focus":
        for im in ax.images:
            im.set_alpha(0.98)
        # Very light accents, or you can comment this out if you want pure aura
        draw_geometric_accents(ax, emotions, seed=seed, density_scale=0.4)
    else:  # "Hybrid"
        for im in ax.images:
            im.set_alpha(0.90)
        draw_geometric_accents(ax, emotions, seed=seed, density_scale=0.9)

    ax.set_title("Aura Tarot Poster", pad=10)
    return fig
