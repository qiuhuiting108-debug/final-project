"""
generator.py

Hybrid generative poster engine that combines:
- A soft aura-style background field.
- A lighter, more minimal geometric layer.

This version focuses more on aesthetic composition:
- Fewer rectangles
- More negative space
- Softer pastel palette
"""

from typing import Dict
import random

import numpy as np
import matplotlib.pyplot as plt


# ---- Palette helpers ------------------------------------------------------


def get_pastel_palette():
    """
    Soft pastel palette, good for dreamy / aura visuals.
    """
    return [
        (0.88, 0.69, 0.77),  # rose
        (0.69, 0.80, 0.91),  # sky blue
        (0.76, 0.86, 0.78),  # soft green
        (0.97, 0.86, 0.68),  # peach
        (0.86, 0.80, 0.92),  # lavender
        (0.98, 0.93, 0.78),  # light yellow
    ]


# ---- Aura layer -----------------------------------------------------------


def generate_aura_layer(ax, emotions: Dict[str, float], resolution: int = 500):
    """
    Draw an aura-style layer using a smooth 2D field
    with radial and wave-like components.
    The result is normalized and mapped into a soft RGB field.
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    x = np.linspace(-1.4, 1.4, resolution)
    y = np.linspace(-1.4, 1.4, resolution)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    # Base glow
    field = np.exp(-R**2 * (1.8 - 0.8 * calm))

    # Desire & connection as off-center glows
    field += 0.7 * desire * np.exp(-((X - 0.4)**2 + (Y + 0.2)**2) * 3)
    field += 0.7 * connection * np.exp(-((X + 0.5)**2 + (Y - 0.3)**2) * 3)

    # Mystery & fear as wave perturbations
    field += 0.35 * mystery * np.sin(7 * R + 4 * X) * np.exp(-R**2 * 1.8)
    field += 0.25 * fear * np.cos(9 * R + 3 * Y) * np.exp(-R**2 * 1.6)

    # Transformation as overall brightness & subtle ring
    field += 0.25 * transform * np.exp(-((R - 0.7)**2) * 8)

    # Color channels: cool/warm balance
    cool = 0.3 + 0.4 * calm + 0.4 * mystery + 0.2 * fear
    warm = 0.2 + 0.6 * desire + 0.5 * connection
    mid = 0.3 + 0.4 * connection + 0.3 * transform

    R_ch = warm * field
    G_ch = mid * field
    B_ch = cool * field

    img = np.stack([R_ch, G_ch, B_ch], axis=2)
    img = img - img.min()
    img = img / (img.max() + 1e-6)

    # Slight overall brightness boost
    img = np.clip(img * (0.9 + 0.4 * transform), 0, 1)

    ax.imshow(img, extent=(0, 1, 0, 1), origin="lower")


# ---- Geometric layer ------------------------------------------------------


def generate_geometric_layer(ax, emotions: Dict[str, float], seed: int = 0):
    """
    Draw a lighter geometric layer:
    - Fewer rectangles
    - More transparency
    - Softer pastel colors
    """
    random.seed(seed)
    np.random.seed(seed)

    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    transform = emotions["Transformation"]

    palette = get_pastel_palette()

    # Fewer cells for more negative space
    base_cells = 4
    extra_cells = int(transform * 3)  # 0–3 more
    cells = base_cells + extra_cells  # 4–7

    for i in range(cells):
        for j in range(cells):
            # Randomly skip many cells to avoid overcrowding
            skip_prob = 0.45 + 0.25 * calm  # more calm → more empty space
            if random.random() < skip_prob:
                continue

            x = i / cells
            y = j / cells
            w = 1.0 / cells
            h = 1.0 / cells

            # Transparency: less fear + desire → lighter layer
            alpha = 0.06 + 0.25 * (fear + desire)

            color = random.choice(palette)

            jitter_x = (random.random() - 0.5) * w * 0.35
            jitter_y = (random.random() - 0.5) * h * 0.35

            rect_w = w * (0.6 + 0.7 * random.random())
            rect_h = h * (0.6 + 0.7 * random.random())

            rect = plt.Rectangle(
                (x + jitter_x, y + jitter_y),
                rect_w,
                rect_h,
                linewidth=0,
                color=color,
                alpha=alpha,
            )
            ax.add_patch(rect)


# ---- Public API -----------------------------------------------------------


def generate_hybrid_poster(
    emotions: Dict[str, float],
    style: str = "Hybrid",
    seed: int = 0
):
    """
    Generate a hybrid poster where:
    - The background is a smooth, dreamy aura field.
    - The foreground uses a minimal geometric layer.

    Styles:
        "Hybrid"           – balanced aura + geometry
        "Geometric Focus"  – slightly stronger geometry, lighter aura
        "Aura Focus"       – aura dominates, very light geometry
    """
    fig, ax = plt.subplots(figsize=(4.5, 6.5))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    # Background aura
    generate_aura_layer(ax, emotions, resolution=520)

    # Adjust aura visibility depending on style
    if style == "Geometric Focus":
        for im in ax.images:
            im.set_alpha(0.7)
    elif style == "Aura Focus":
        for im in ax.images:
            im.set_alpha(0.95)
    else:  # Hybrid
        for im in ax.images:
            im.set_alpha(0.85)

    # Geometric layer
    generate_geometric_layer(ax, emotions, seed=seed)

    ax.set_title("Aura Tarot Poster", pad=10)
    return fig

