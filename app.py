import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import random

st.set_page_config(page_title="Dream Visualizer", layout="wide")

st.title("✨ Dream Visualizer — Abstract Generative Poster")

st.write("Describe your dream, and the AI will transform it into an abstract generative poster.")


# -----------------------------
# Poster Style Color Palettes
# -----------------------------
def get_style_colors(style):
    if style == "Emotional Bloom":
        return ["#ff66cc", "#ff99dd", "#cc66ff", "#aa44ff", "#550088"]
    elif style == "Energy Waves":
        return ["#ff8c00", "#ff4500", "#ff0055", "#ffaa00", "#ffdd55"]
    elif style == "Cosmic Spiral":
        return ["#00ccff", "#0066ff", "#6600ff", "#330066", "#000022"]
    elif style == "Neon Aura":
        return ["#39ff14", "#00ffea", "#ff00e1", "#ffea00", "#00c3ff"]
    else:
        return ["#ffffff"]


# -----------------------------
# Abstract Art Generator
# -----------------------------
def generate_poster(text, style):
    seed = abs(hash(text)) % (10**8)
    np.random.seed(seed)
    random.seed(seed)

    fig, ax = plt.subplots(figsize=(10, 14))
    ax.set_facecolor("#000000")
    ax.axis("off")

    colors = get_style_colors(style)

    steps = 5000
    angles = np.linspace(0, 8*np.pi, steps)
    radius = np.abs(np.sin(angles * random.uniform(0.3, 1.5))) * random.uniform(0.5, 1.3)

    x = radius * np.cos(angles)
    y = radius * np.sin(angles)

    for i in range(steps):
        ax.scatter(
            x[i] + np.random.uniform(-0.03, 0.03),
            y[i] + np.random.uniform(-0.03, 0.03),
            s=random.uniform(5, 40),
            color=colors[i % len(colors)],
            alpha=random.uniform(0.06, 0.5),
        )

    return fig


# -----------------------------
# UI
# -----------------------------
dream_text = st.text_area("📝 Enter your dream description:", height=150)

style = st.selectbox(
    "🎨 Choose poster style",
    ["Emotional Bloom", "Energy Waves", "Cosmic Spiral", "Neon Aura"]
)

generate_btn = st.button("Generate Poster")


# -----------------------------
# Run Generator
# -----------------------------
if generate_btn:
    if not dream_text.strip():
        st.error("Please enter your dream.")
    else:
        with st.spinner("🎨 Generating your personalized poster..."):
            fig = generate_poster(dream_text, style)
            st.pyplot(fig)
