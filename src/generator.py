import numpy as np
import matplotlib.pyplot as plt
import random

def generate_abstract_art(text, style="Energy Waves"):
    np.random.seed(abs(hash(text)) % (10**8))
    random.seed(abs(hash(text)) % (10**8))

    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_facecolor("#000000")
    ax.axis("off")

    steps = 8000
    angles = np.linspace(0, 6*np.pi, steps)
    radius = np.abs(np.sin(angles * random.uniform(0.5, 2))) * random.uniform(0.3, 1.2)

    x = radius * np.cos(angles + random.random())
    y = radius * np.sin(angles + random.random())

    colors = get_style_color(style)

    for i in range(steps):
        ax.scatter(
            x[i] + np.random.uniform(-0.05, 0.05),
            y[i] + np.random.uniform(-0.05, 0.05),
            color=colors[i % len(colors)],
            s=random.uniform(5, 60),
            alpha=random.uniform(0.05, 0.4)
        )

    return fig


def get_style_color(style):
    if style == "Energy Waves":
        return ["#ff8c00", "#ff4500", "#ff0055", "#ffaa00", "#ffdd55"]
    elif style == "Emotional Bloom":
        return ["#ff66cc", "#ff99dd", "#cc66ff", "#aa44ff", "#550088"]
    elif style == "Cosmic Spiral":
        return ["#00ccff", "#0066ff", "#6600ff", "#330066", "#000022"]
    elif style == "Chaos Flow":
        return ["#33ff99", "#00cc66", "#00994d", "#006633", "#00331a"]
    elif style == "Neon Aura":
        return ["#39ff14", "#00ffea", "#ff00e1", "#ffea00", "#00c3ff"]
    else:
        return ["#ffffff"]
