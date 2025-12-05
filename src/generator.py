"""
generator.py

Hybrid generative poster engine that combines:
- An aura-style background field.
- A geometric rectangle grid on top.

The visual parameters are driven by the 6D emotion model.
"""

from typing import Dict
import random

import numpy as np
import matplotlib.pyplot as plt


def generate_geometric_layer(ax, emotions: Dict[str, float], seed: int = 0):
    """
    Draw a geometric generative poster layer:
    - Grid of rectangles
    - Sizes and jitter influenced by emotions
    """
    random.seed(seed)
    np.random.seed(seed)

    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    transform = emotions["Transformation"]

    palette = [
        (0.23, 0.36, 0.63),   # deep blue
        (0.91, 0.33, 0.51),   # pink-red
        (0.50, 0.73, 0.90),   # sky blue
        (0.98, 0.68, 0.32),   # orange
        (0.84, 0.72, 0.88),   # soft purple
        (0.97, 0.93, 0.64),   # light yellow
    ]

    base_cells = 6
    extra_cells = int(transform * 6)
    cells = base_cells + extra_cells

    for i in range(cells):
        for j in range(cells):
            x = i / cells
            y = j / cells
            w = 1.0 / cells
            h = 1.0 / cells

            # keep some gaps based on calm
            if random.random() < 0.2 * calm:
                continue

            alpha = 0.1 + 0.4 * (fear + desire)
            color = random.choice(palette)

            jitter_x = (random.random() - 0.5) * w * 0.3
            jitter_y = (random.random() - 0.5) * h * 0.3

            rect = plt.Rectangle(
                (x + jitter_x, y + jitter_y),
                w * (0.7 + 0.6 * random.random()),
                h * (0.7 + 0.6 * random.random()),
                linewidth=0,
                color=color,
                alpha=alpha,
            )
            ax.add_patch(rect)


def generate_aura_layer(ax, emotions: Dict[str, float], resolution: int = 400):
    """
    Draw an aura-style layer using a smooth 2D field
    with radial and wave-like components.
    """
    fear = emotions["Fear"]
    desire = emotions["Desire"]
    calm = emotions["Calm"]
    mystery = emotions["Mystery"]
    connection = emotions["Connection"]
    transform = emotions["Transformation"]

    x = np.linspace(-1.5, 1.5, resolution)
    y = np.linspace(-1.5, 1.5, resolution)
    X, Y = np.meshgrid(x, y)
    R = np.sqrt(X**2 + Y**2)

    field = np.exp(-R**2 * (2 + 3 * fear)) * (0.6 + 0.7 * calm)
    field += 0.8 * desire * np.exp(-((X - 0.4)**2 + (Y + 0.3)**2) * 4)
    field += 0.8 * connection * np.exp(-((X + 0.5)**2 + (Y - 0.2)**2) * 4)
    field += 0.3 * mystery * np.sin(8 * R + 3 * X) * np.exp(-R**2 * 2)
    field += 0.3 * transform * np.cos(10 * R + 2 * Y) * np.exp(-R**2 * 1.5)

    cool = 0.2 + 0.5 * calm + 0.5 * mystery + 0.4 * fear
    warm = 0.2 + 0.6 * desire + 0.5 * connection
    brightness = 0.4 + 0.6 * transform

    R_ch = warm * field
    B_ch = cool * field
    G_ch = 0.5 * field * (calm + connection + 0.3)

    img = np.stack([R_ch, G_ch, B_ch], axis=2)
    img = img - img.min()
    img = img / (img.max() + 1e-6)
    img = np.clip(img * brightness, 0, 1)

    ax.imshow(img, extent=(0, 1, 0, 1), origin="lower")


def generate_hybrid_poster(emotions: Dict[str, float], style: str = "Hybrid", seed: int = 0):
    """
    Generate a hybrid poster where:
    - The background is aura-style generative art.
    - The foreground uses geometric rectangles.
    """
    import matplotlib.pyplot as plt  # local to avoid circular issues
    import numpy as np               # for safety if needed later

    fig, ax = plt.subplots(figsize=(5, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    generate_aura_layer(ax, emotions, resolution=400)

    if style == "Geometric Focus":
        for im in ax.images:
            im.set_alpha(0.6)
        generate_geometric_layer(ax, emotions, seed=seed)
    elif style == "Aura Focus":
        for im in ax.images:
            im.set_alpha(0.9)
        generate_geometric_layer(ax, emotions, seed=seed)
    else:  # Hybrid
        for im in ax.images:
            im.set_alpha(0.75)
        generate_geometric_layer(ax, emotions, seed=seed)

    ax.set_title("Aura Tarot Poster", pad=12)
    return fig
