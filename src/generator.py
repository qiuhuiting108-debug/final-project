"""
generator.py

Generative abstract poster engine for the
Aura Tarot Dream Analyzer.

This version is closer to:
- Chakra / aura paintings
- Swirling, flowing textures
- Multiple energy cores along a vertical axis

Styles:
    "Aura Focus"       -> pure aura / flow field, no rectangles
    "Hybrid"           -> aura + a few soft rectangles
    "Geometric Focus"  -> aura + slightly stronger geometry
"""

from typing import Dict
import random

import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Helper: map emotions -> colormap
# ---------------------------------------------------------------------


def choose_cmap(emotions: Dict[str, float]) -> str:
    """
    Map the emotion vector to a matplotlib colormap.
    Try to reflect mood:
    - Fear + Mystery  high  -> darker / mystical maps
    - Desire + Connection high -> warm / bright maps
    - Calm high -> clean cool maps
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    s = fear + desire + calm + mystery + connection + transform + 1e-6
    fear_n = fear / s
    desire_n = desire / s
    calm_n = calm / s
    mystery_n = mystery / s
    conn_n = connection / s

    if fear_n + mystery_n > 0.55:
        return "twilight_shifted"
    if desire_n + conn_n > 0.55:
        return "plasma"
    if calm_n > 0.45:
        return "viridis"
    # mixed / introspective
    return "magma"


# ---------------------------------------------------------------------
# Aura / flow field
# ---------------------------------------------------------------------


def generate_aura_field(emotions: Dict[str, float], resolution: int = 700):
    """
    Create a 2D scalar field that feels like:
    - multiple energy cores (chakra-like)
    - concentric waves and angular swirls
    - fine line-like texture
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    x = np.linspace(-1.5, 1.5, resolution)
    y = np.linspace(-2.0, 2.0, resolution)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)
    theta = np.arctan2(Y, X)

    # --- 1. vertical "spine" of energy cores ---------------------------
    # positions along Y axis (like head / heart / belly)
    core_y_positions = [-1.0, -0.2, 0.8]
    core_strengths = [
        0.5 + 0.8 * fear,        # lower core -> survival / fear
        0.5 + 0.8 * connection,  # middle core -> relation
        0.5 + 0.8 * desire,      # upper core -> longing / imagination
    ]

    spine_field = np.zeros_like(X)
    for y0, strength in zip(core_y_positions, core_strengths):
        spine_field += strength * np.exp(-((X * 0.6)**2 + (Y - y0)**2) * 4.0)

    # --- 2. global radial glow -----------------------------------------
    base = np.exp(-R**2 * (1.4 + 1.0 * fear - 0.7 * calm))

    # --- 3. swirling rings (transformation) ----------------------------
    rings = np.cos(10 * R - 4 * transform) * np.exp(-R**2 * 2.3)

    # --- 4. angular flows (mystery) ------------------------------------
    angular = np.sin(6 * theta + 5 * R) * np.exp(-R**2 * 1.5)

    # --- 5. fine "stroke" texture --------------------------------------
    # high-frequency directional noise to mimic many short strokes
    tex = (
        np.sin(14 * X + 9 * Y)
        + 0.7 * np.sin(18 * Y - 11 * X)
        + 0.5 * np.sin(22 * R + 7 * theta)
    )
    tex *= np.exp(-R**2 * 1.6)
    # strength of strokes mainly driven by transformation & mystery
    tex_strength = 0.18 + 0.35 * (transform + mystery)

    field = (
        0.9 * base
        + 0.8 * spine_field
        + 0.5 * transform * rings
        + 0.5 * mystery * angular
        + tex_strength * tex
    )

    # if emotions overall are low, add a gentle center glow to avoid flatness
    total_emotion = fear + desire + calm + mystery + connection + transform
    if total_emotion < 0.6:
        field += 0.25 * np.exp(-((X * 0.7)**2 + (Y * 0.7)**2) * 3.0)

    # normalize to 0–1
    field = field - field.min()
    field = field / (field.max() + 1e-6)
    return field


def draw_aura_layer(ax, emotions: Dict[str, float], resolution: int = 700):
    """
    Draw the aura / flow field using a colormap chosen by emotions.
    """
    cmap_name = choose_cmap(emotions)
    field = generate_aura_field(emotions, resolution=resolution)

    ax.imshow(
        field,
        cmap=cmap_name,
        extent=(0, 1, 0, 1),
        origin="lower",
        interpolation="bilinear",
    )
    return field


# ---------------------------------------------------------------------
# Geometric accents (optional)
# ---------------------------------------------------------------------


def draw_geometric_accents(
    ax,
    emotions: Dict[str, float],
    seed: int = 0,
    density_scale: float = 1.0,
):
    """
    Very light geometric accents to add a contemporary layer.
    If style is Aura Focus, we won't call this at all.
    """
    random.seed(seed)
    np.random.seed(seed)

    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    transform = emotions["Transformation"]

    palette = [
        (0.96, 0.78, 0.82),  # soft pink
        (0.80, 0.86, 0.97),  # light blue
        (0.88, 0.92, 0.80),  # gentle green
        (0.98, 0.88, 0.72),  # peach
        (0.88, 0.82, 0.96),  # lavender
    ]

    base_n = int(5 * density_scale)
    extra_n = int(8 * transform * density_scale)
    n_shapes = base_n + extra_n

    for _ in range(n_shapes):
        if random.random() < 0.35 + 0.3 * calm:
            continue

        cx = random.uniform(0.15, 0.85)
        cy = random.uniform(0.1, 0.9)

        base_size = 0.07 + 0.10 * (fear + desire)
        w = base_size * random.uniform(0.7, 1.5)
        h = base_size * random.uniform(0.6, 1.5)

        alpha = 0.05 + 0.20 * (fear + desire)

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
    Entry point used by the Streamlit app.

    style:
        "Aura Focus"       -> pure aura / flow field (no rectangles)
        "Hybrid"           -> aura + a few soft rectangles
        "Geometric Focus"  -> aura + more accents
    """
    fig, ax = plt.subplots(figsize=(4.5, 7.0))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # draw aura first
    field = draw_aura_layer(ax, emotions, resolution=720)

    # adjust visibility & accents depending on style
    if style == "Geometric Focus":
        for im in ax.images:
            im.set_alpha(0.80)
        draw_geometric_accents(ax, emotions, seed=seed, density_scale=1.5)
    elif style == "Aura Focus":
        for im in ax.images:
            im.set_alpha(0.98)
        # no rectangles here: pure aura
    else:  # Hybrid
        for im in ax.images:
            im.set_alpha(0.90)
        draw_geometric_accents(ax, emotions, seed=seed, density_scale=0.9)

    ax.set_title("Aura Tarot Poster", pad=12)
    return fig
