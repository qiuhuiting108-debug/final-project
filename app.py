import streamlit as st
from io import BytesIO

# import local modules from src/
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

    # -----------------------------
    # Title & high-level description
    # -----------------------------
    st.title("💫 Aura Tarot Dream Analyzer")

    st.markdown(
        """
This app turns your **dream text** into:

1. Simple **symbol parsing**  
2. Six-dimensional **emotional factors**  
3. Visual outputs:
   - Symbol explanations  
   - Emotion **radar chart**  
   - **Aura energy bar**  
   - Abstract **Aura poster**  
   - Tarot-style **interpretation text**  
4. A download button for your Aura poster (PNG)
"""
    )

    # -----------------------------
    # Sidebar: style selection
    # -----------------------------
    with st.sidebar:
        st.header("Settings")
        style = st.selectbox(
            "Aura style",
            ["Mystic", "Pastel", "Cyber", "Golden"],
            index=0,
        )
        st.markdown(
            """
**Aura Styles**

- *Mystic*: deep, cosmic tones  
- *Pastel*: soft, dreamy colors  
- *Cyber*: high contrast, neon-like  
- *Golden*: warm, ritual-like glow  
"""
        )

    # -----------------------------
    # Step 1 – Input dream text
    # -----------------------------
    st.subheader("1. Input dream text")
    dream_text = st.text_area(
        "Write a short description of your dream (any language is okay).",
        height=200,
        placeholder=(
            "Example: I was running in a dark train station, wearing a white dress. "
            "The sea was below the bridge and I was afraid of falling..."
        ),
    )

    analyze = st.button("✨ Analyze Dream")

    # If button not clicked, just show instructions
    if not analyze:
        st.info("Write your dream above and click **“✨ Analyze Dream”** to see all results.")
        return

    if not dream_text.strip():
        st.warning("Please write something about your dream first.")
        return

    # =====================================================
    # 2. Simple symbol parsing
    # =====================================================
    st.subheader("2. Simple symbol parsing")
    symbols = analyze_symbols(dream_text)

    if symbols:
        st.write("Detected symbols and their meanings:")
        for s in symbols:
            explanation = SYMBOLS.get(s, "")
            st.markdown(f"- **{s.capitalize()}** — {explanation}")
    else:
        st.write(
            "No predefined symbols were detected, "
            "but your dream will still be analyzed on the emotional level."
        )

    # =====================================================
    # 3. Emotional model – six-dimensional factors
    # =====================================================
    st.subheader("3. Six emotional factors")
    emotion_scores = extract_emotions(dream_text)

    cols = st.columns(len(EMOTIONS))
    for col, emo in zip(cols, EMOTIONS):
        with col:
            st.metric(emo, f"{emotion_scores[emo]:.2f}")

    # -----------------------------------------------------
    # 3-1. Emotion radar chart
    # -----------------------------------------------------
    st.markdown("**Emotion radar chart**")
    radar_fig = create_radar_chart(emotion_scores)
    st.pyplot(radar_fig)

    # -----------------------------------------------------
    # 3-2. Aura energy bar
    # -----------------------------------------------------
    st.markdown("**Aura energy bar**")
    aura_fig = create_aura_bar(emotion_scores, style)
    st.pyplot(aura_fig)

    # =====================================================
    # 4. Generative Aura poster
    # =====================================================
    st.subheader("4. Generative Aura poster")
    poster_fig = create_aura_poster(emotion_scores, style)
    st.pyplot(poster_fig)

    # Download button for poster
    buf = BytesIO()
    poster_fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
    buf.seek(0)
    st.download_button(
        label="📥 Download Aura Poster (PNG)",
        data=buf,
        file_name="aura_dream_poster.png",
        mime="image/png",
    )

    # =====================================================
    # 5. Tarot-style interpretation
    # =====================================================
    st.subheader("5. Tarot-style interpretation")

    shadow_text, energy_text, guidance_text = generate_tarot_reading(
        symbols, emotion_scores
    )

    st.markdown("**Shadow – Subconscious message**")
    st.write(shadow_text)

    st.markdown("**Energy – Current emotional flow**")
    st.write(energy_text)

    st.markdown("**Guidance – Supportive insight**")
    st.write(guidance_text)

    st.success("Done! You can scroll up to review all layers of your dream analysis.")


if __name__ == "__main__":
    main()
