import os
import hashlib

import streamlit as st

from src.analyzer import analyze_dream
from src.viz import plot_emotion_radar, plot_emotion_spectrum
from src.generator import generate_hybrid_poster


# -------------------------------------------------------
# Page config
# -------------------------------------------------------
st.set_page_config(
    page_title="Aura Tarot Dream Analyzer",
    page_icon="✨",
    layout="wide",
)


# -------------------------------------------------------
# Title & Intro
# -------------------------------------------------------
st.title("✨ Aura Tarot Dream Analyzer")
st.caption("Final Project — Arts & Advanced Big Data | Huiting Qiu")

st.markdown(
    """
This app turns your dream into:

1. **A symbolic interpretation** (AI or rule-based)
2. **A 6-dimensional emotional profile** (Fear, Desire, Calm, Mystery, Connection, Transformation)
3. **Visualizations** (radar chart + aura spectrum)
4. **Generative abstract posters** in aura / tarot style
"""
)

st.markdown("---")


# -------------------------------------------------------
# Layout: left controls, right preview
# -------------------------------------------------------
col_left, col_right = st.columns([1.1, 1.4])

with col_left:
    st.subheader("1. Dream Input")

    dream_text = st.text_area(
        "Describe your dream in as much detail as you like (English is recommended for best analysis).",
        height=200,
        placeholder=(
            "Example: I was walking through an endless tunnel. The walls were breathing slowly "
            "and a faint blue light followed me from behind..."
        ),
    )

    st.subheader("2. Poster Settings")

    poster_style = st.selectbox(
        "Poster style",
        options=["Hybrid", "Aura Focus", "Geometric Focus"],
        index=0,
        help=(
            "Aura Focus: mostly aura / energy field\n"
            "Hybrid: aura + a few soft rectangles\n"
            "Geometric Focus: stronger geometric accents"
        ),
    )

    multi_variation = st.checkbox(
        "Generate two poster variations",
        value=True,
        help="If checked, you will see two posters with slightly different seeds.",
    )

    analyze_button = st.button("🔮 Analyze Dream & Generate Posters")


with col_right:
    st.subheader("Live Preview Note")
    st.write(
        "After you click **Analyze** on the left, the emotional analysis, visualizations, "
        "and posters will appear here."
    )


st.markdown("---")


# -------------------------------------------------------
# Helper: deterministic seed from dream text
# -------------------------------------------------------
def dream_to_seed(text: str) -> int:
    """
    Generate a deterministic random seed from the dream text.
    Different dreams -> different seeds.
    Same dream -> same seed (reproducible).
    """
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(h[:8], 16)


# -------------------------------------------------------
# Main logic
# -------------------------------------------------------
if analyze_button:
    if not dream_text.strip():
        st.error("Please type something about your dream before analyzing.")
    else:
        # -----------------------------
        # 1. Analyze dream (AI or rule-based)
        # -----------------------------
        with st.spinner("Analyzing your dream..."):
            result = analyze_dream(dream_text)

        emotions = result.get("emotions", {})
        symbolic_summary = result.get("symbolic_summary", "")
        tarot_shadow = result.get("tarot_shadow", "")
        tarot_energy = result.get("tarot_energy", "")
        tarot_guidance = result.get("tarot_guidance", "")

        # -----------------------------
        # 2. Text interpretation
        # -----------------------------
        st.subheader("2. Interpretation & Tarot Reading")

        col_a, col_b = st.columns(2)

        with col_a:
            st.markdown("**Symbolic Summary**")
            st.write(symbolic_summary)

            st.markdown("**Tarot — Shadow Message**")
            st.write(tarot_shadow)

        with col_b:
            st.markdown("**Tarot — Aura Energy**")
            st.write(tarot_energy)

            st.markdown("**Tarot — Guidance**")
            st.write(tarot_guidance)

        # -----------------------------
        # 3. Emotional visualization
        # -----------------------------
        st.subheader("3. Emotional Profile & Visualization")

        if emotions:
            col_v1, col_v2 = st.columns(2)

            with col_v1:
                radar_fig = plot_emotion_radar(emotions)
                st.pyplot(radar_fig, use_container_width=True)

            with col_v2:
                spectrum_fig = plot_emotion_spectrum(emotions)
                st.pyplot(spectrum_fig, use_container_width=True)
        else:
            st.warning("No emotion data returned from analyzer. Please check analyzer module.")

        # -----------------------------
        # 4. Generative Posters (seed from dream)
        # -----------------------------
        st.subheader("4. Generative Aura Posters")

        seed_base = dream_to_seed(dream_text)

        # Poster Variation 1
        poster_fig_1 = generate_hybrid_poster(
            emotions=emotions,
            style=poster_style,
            seed=seed_base,
        )
        st.markdown("### Poster Variation 1")
        st.pyplot(poster_fig_1, use_container_width=True)

        # Poster Variation 2 (optional)
        if multi_variation:
            poster_fig_2 = generate_hybrid_poster(
                emotions=emotions,
                style=poster_style,
                seed=seed_base + 37,
            )
            st.markdown("### Poster Variation 2")
            st.pyplot(poster_fig_2, use_container_width=True)

        st.success("Done! Different dreams will now produce different posters.")
