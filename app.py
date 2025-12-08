import os
import hashlib

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from src.analyzer import analyze_dream
from src.generator import generate_hybrid_poster


# -------------------------------------------------------
#  Visualization Helpers (No import from src.viz!)
# -------------------------------------------------------
def plot_emotion_radar(emotions: dict):
    """Simple radar chart for 6 emotions."""
    labels = list(emotions.keys())
    values = [emotions[k] for k in labels]

    # close loop
    labels.append(labels[0])
    values.append(values[0])

    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)

    fig, ax = plt.subplots(subplot_kw={"polar": True}, figsize=(4, 4))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels[:-1])
    ax.set_yticklabels([])
    ax.set_title("Emotion Radar", pad=12)

    return fig


def plot_emotion_spectrum(emotions: dict):
    """Simple horizontal bar 'emotion spectrum'."""
    labels = list(emotions.keys())
    values = [emotions[k] for k in labels]

    fig, ax = plt.subplots(figsize=(4, 4))
    bars = ax.barh(labels, values, color="purple", alpha=0.6)
    ax.set_xlim(0, 1)
    ax.set_title("Emotion Spectrum")
    for bar, v in zip(bars, values):
        ax.text(v + 0.02, bar.get_y() + bar.get_height() / 2, f"{v:.2f}", va="center")
    plt.tight_layout()
    return fig


# -------------------------------------------------------
# Page config
# -------------------------------------------------------
st.set_page_config(
    page_title="Aura Tarot Dream Analyzer",
    page_icon="✨",
    layout="wide",
)


# -------------------------------------------------------
# UI
# -------------------------------------------------------
st.title("✨ Aura Tarot Dream Analyzer")
st.caption("Final Project — Arts & Advanced Big Data | Huiting Qiu")

st.markdown(
    """
This app turns your dream into:

1. **A symbolic interpretation**  
2. **A 6-dimensional emotional profile**  
3. **Visualizations (Radar + Spectrum)**  
4. **Generative Dream Aura Posters**

Different dreams → different posters.
"""
)

st.markdown("---")

col_left, col_right = st.columns([1.1, 1.4])


# ------------------------- LEFT PANEL -------------------------
with col_left:
    st.subheader("1. Dream Input")

    dream_text = st.text_area(
        "Describe your dream:",
        height=200,
        placeholder="Example: I was walking in a glowing forest where the trees were breathing...",
    )

    st.subheader("2. Poster Settings")

    poster_style = st.selectbox(
        "Poster Style",
        options=["Hybrid", "Aura Focus", "Geometric Focus"],
        index=0,
    )

    multi_variation = st.checkbox(
        "Generate two poster variations",
        value=True,
    )

    analyze_button = st.button("🔮 Analyze Dream & Generate Posters")


# ------------------------- RIGHT PANEL -------------------------
with col_right:
    st.subheader("Preview Panel")
    st.write("Your analysis & posters will appear here after clicking **Analyze**.")


st.markdown("---")


# -------------------------------------------------------
#  Dream → deterministic seed
# -------------------------------------------------------
def dream_to_seed(text: str) -> int:
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


# -------------------------------------------------------
#  Main Logic
# -------------------------------------------------------
if analyze_button:
    if not dream_text.strip():
        st.error("Please enter a dream description first.")
    else:
        # -----------------------------
        # 1. Analyze Dream
        # -----------------------------
        with st.spinner("Analyzing your dream..."):
            result = analyze_dream(dream_text)

        emotions = result.get("emotions", {})
        symbolic_summary = result.get("symbolic_summary", "")
        tarot_shadow = result.get("tarot_shadow", "")
        tarot_energy = result.get("tarot_energy", "")
        tarot_guidance = result.get("tarot_guidance", "")

        # -----------------------------
        # 2. Interpretation
        # -----------------------------
        st.subheader("2. Interpretation & Tarot Reading")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("### Symbolic Summary")
            st.write(symbolic_summary)

            st.markdown("### Tarot — Shadow Message")
            st.write(tarot_shadow)

        with col_b:
            st.markdown("### Tarot — Aura Energy")
            st.write(tarot_energy)

            st.markdown("### Tarot — Guidance")
            st.write(tarot_guidance)

        # -----------------------------
        # 3. Visualization
        # -----------------------------
        st.subheader("3. Emotional Visualization")

        if emotions:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                radar_fig = plot_emotion_radar(emotions)
                st.pyplot(radar_fig, use_container_width=True)

            with col_v2:
                spectrum_fig = plot_emotion_spectrum(emotions)
                st.pyplot(spectrum_fig, use_container_width=True)
        else:
            st.warning("No emotion data returned.")

        # -----------------------------
        # 4. Posters (dream-dependent seed)
        # -----------------------------
        st.subheader("4. Generative Dream Aura Posters")

        seed_base = dream_to_seed(dream_text)

        # Variation 1
        poster_fig_1 = generate_hybrid_poster(
            emotions=emotions,
            style=poster_style,
            seed=seed_base,
        )
        st.markdown("### Poster Variation 1")
        st.pyplot(poster_fig_1, use_container_width=True)

        # Variation 2
        if multi_variation:
            poster_fig_2 = generate_hybrid_poster(
                emotions=emotions,
                style=poster_style,
                seed=seed_base + 37,
            )
            st.markdown("### Poster Variation 2")
            st.pyplot(poster_fig_2, use_container_width=True)

        st.success("Done! Different dreams will now generate different posters.")

