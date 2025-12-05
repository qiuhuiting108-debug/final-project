"""
app.py

Streamlit front-end for the Aura Tarot Dream Analyzer.

It connects:
- Dream analysis (OpenAI + rule-based fallback)
- Emotion visualization (radar + spectrum)
- Generative poster engine (hybrid aura + geometry)
"""

from io import BytesIO

import streamlit as st

from src.analyzer import analyze_dream
from src.viz import plot_emotion_radar, plot_aura_bar
from src.generator import generate_hybrid_poster


st.set_page_config(
    page_title="Aura Tarot Dream Analyzer",
    page_icon="🌙",
    layout="wide",
)

st.title("🌙 Aura Tarot Dream Analyzer")
st.markdown(
    """
Turn your dream into **emotional data, generative posters, and tarot-style insight**.

This app is designed as an **all-in-one final project** for the course
*Arts & Advanced Big Data*, combining:

- AI text analysis (dream & tarot reading)
- Data-driven emotion modeling
- Visualization (radar chart + aura spectrum)
- Generative art (hybrid geometric + aura poster)
- Interactive web interface (Streamlit)
"""
)

with st.sidebar:
    st.header("Settings")
    poster_style = st.selectbox(
        "Poster Style",
        ["Hybrid", "Geometric Focus", "Aura Focus"],
        help="Change the balance between geometry and aura visuals.",
    )
    multi_variation = st.checkbox(
        "Generate two poster variations",
        value=True,
        help="If checked, the app will create two posters with different random seeds.",
    )

dream_text = st.text_area(
    "Describe your dream here:",
    height=200,
    placeholder=(
        "Example: I was on a crowded train above the ocean. "
        "The sky was turning darker and I was afraid of being late for an exam. "
        "Suddenly, a door of light appeared at the end of the train..."
    ),
)

analyze_button = st.button("🔮 Analyze My Dream", type="primary")

if analyze_button:
    if not dream_text.strip():
        st.warning("Please enter a dream description first.")
    else:
        # --- 1. Analyze dream (OpenAI + fallback) ---
        result, model_used = analyze_dream(dream_text)

        symbolic_summary = result["symbolic_summary"]
        emotions = result["emotions"]
        tarot_shadow = result["tarot_shadow"]
        tarot_energy = result["tarot_energy"]
        tarot_guidance = result["tarot_guidance"]

        # --- 2. Layout: interpretation & visualization ---
        col1, col2 = st.columns([1.2, 1])

        with col1:
            st.subheader("1. Dream Interpretation")
            st.markdown(f"**Analysis Model Used:** {model_used}")
            st.markdown("**Symbolic Summary**")
            st.write(symbolic_summary)

            st.subheader("2. Aura Tarot Reading")
            st.markdown(f"**Shadow (Subconscious Message)**\n\n{tarot_shadow}")
            st.markdown(f"**Energy (Current Aura)**\n\n{tarot_energy}")
            st.markdown(f"**Guidance**\n\n{tarot_guidance}")

        with col2:
            st.subheader("3. Emotional Data")
            radar_fig = plot_emotion_radar(emotions)
            st.pyplot(radar_fig, use_container_width=True)

            aura_bar_fig = plot_aura_bar(emotions)
            st.pyplot(aura_bar_fig, use_container_width=True)

        # --- 3. Posters ---
        st.subheader("4. Generative Aura Posters")

        poster_fig_1 = generate_hybrid_poster(emotions, style=poster_style, seed=0)
        st.markdown("**Poster Variation 1**")
        st.pyplot(poster_fig_1, use_container_width=True)

        poster_fig_2 = None
        if multi_variation:
            poster_fig_2 = generate_hybrid_poster(emotions, style=poster_style, seed=7)
            st.markdown("**Poster Variation 2**")
            st.pyplot(poster_fig_2, use_container_width=True)

        # --- 4. Download buttons ---
        st.subheader("5. Download Posters")

        buf1 = BytesIO()
        poster_fig_1.savefig(buf1, format="png", dpi=300, bbox_inches="tight")
        buf1.seek(0)
        st.download_button(
            label="Download Poster 1 (PNG)",
            data=buf1,
            file_name="aura_tarot_poster_1.png",
            mime="image/png",
        )

        if poster_fig_2 is not None:
            buf2 = BytesIO()
            poster_fig_2.savefig(buf2, format="png", dpi=300, bbox_inches="tight")
            buf2.seek(0)
            st.download_button(
                label="Download Poster 2 (PNG)",
                data=buf2,
                file_name="aura_tarot_poster_2.png",
                mime="image/png",
            )

        st.success("Analysis complete. Scroll up and down to explore all sections.")
else:
    st.info("Describe a dream and click **Analyze My Dream** to begin.")
