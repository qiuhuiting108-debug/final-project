import streamlit as st
from io import BytesIO

from src.emotion_model import EMOTIONS, extract_emotions
from src.analyzer import SYMBOLS, analyze_symbols, generate_tarot_reading
from src.viz import create_radar_chart, create_aura_bar
from src.generator import create_aura_poster


def main():
    st.set_page_config(
        page_title="Aura Tarot Dream Analyzer",
        page_icon="💫",
        layout="centered",
    )

    st.title("💫 Aura Tarot Dream Analyzer")
    st.write(
        "Transform your dream into **symbols, emotional data, aura colors,** "
        "and a **generative art poster**."
    )

    # Sidebar
    with st.sidebar:
        st.header("Settings")
        style = st.selectbox(
            "Aura style",
            ["Mystic", "Pastel", "Cyber", "Golden"],
            index=0,
        )
        st.markdown(
            """
            **Styles**
            - *Mystic*: deep, cosmic tones  
            - *Pastel*: soft, dreamy colors  
            - *Cyber*: high contrast, neon-like  
            - *Golden*: warm, ritual-like glow  
            """
        )

    # Input
    st.subheader("1. Describe your dream")
    dream_text = st.text_area(
        "Write a short description of your dream (any language is okay).",
        height=200,
        placeholder=(
            "Example: I was running in a dark train station, wearing a white dress. "
            "The sea was below the bridge and I was afraid of falling..."
        ),
    )

    generate = st.button("✨ Generate Dream Analysis")

    if not generate:
        return

    if not dream_text.strip():
        st.warning("Please write something about your dream first.")
        return

    # ===== Layer 1: Symbolic interpretation =====
    symbols = analyze_symbols(dream_text)

    st.subheader("2. Symbolic Interpretation – What you saw")
    if symbols:
        for s in symbols:
            explanation = SYMBOLS.get(s, "")
            st.markdown(f"- **{s.capitalize()}** — {explanation}")
    else:
        st.write(
            "No specific symbols from the predefined list were detected, "
            "but your dream still carries emotional meaning through the next layers."
        )

    # ===== Layer 2: Emotional factors =====
    emotion_scores = extract_emotions(dream_text)

    st.subheader("3. Emotional Factors – What you felt")
    cols = st.columns(len(EMOTIONS))
    for col, emo in zip(cols, EMOTIONS):
        with col:
            st.metric(emo, f"{emotion_scores[emo]:.2f}")

    radar_fig = create_radar_chart(emotion_scores)
    st.pyplot(radar_fig)

    aura_fig = create_aura_bar(emotion_scores, style)
    st.pyplot(aura_fig)

    # ===== Layer 3: Generative Aura Poster =====
    st.subheader("4. Generative Aura Art Poster – Emotional DNA")
    poster_fig = create_aura_poster(emotion_scores, style)
    st.pyplot(poster_fig)

    buf = BytesIO()
    poster_fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    st.download_button(
        label="📥 Download Aura Poster (PNG)",
        data=buf,
        file_name="aura_dream_poster.png",
        mime="image/png",
    )

    # ===== Layer 4: Tarot-style reading =====
    st.subheader("5. Aura Tarot Interpretation – What it means")
    shadow_text, energy_text, guidance_text = generate_tarot_reading(
        symbols, emotion_scores
    )

    st.markdown("**Shadow – Subconscious message**")
    st.write(shadow_text)

    st.markdown("**Energy – Current emotional flow**")
    st.write(energy_text)

    st.markdown("**Guidance – Supportive insight**")
    st.write(guidance_text)

    st.success(
        "Analysis complete. Scroll up to review each layer, and download your aura poster if you like."
    )


if __name__ == "__main__":
    main()
