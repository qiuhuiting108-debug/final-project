import streamlit as st
from io import BytesIO

# local modules from src/
from src.emotion_model import EMOTIONS, extract_emotions
from src.analyzer import SYMBOLS, analyze_symbols, generate_tarot_reading
from src.viz import create_radar_chart, create_aura_bar
from src.generator import create_aura_poster

# Optional OpenAI client (for aura title & caption)
try:
    from openai import OpenAI
except Exception:  # optional dependency
    OpenAI = None


def generate_openai_aura_title(api_key: str, dream_text: str, emotion_scores: dict):
    """
    Use OpenAI (if api_key is provided) to generate a poetic aura title
    and one-line caption. Returns (title, caption) or (None, None).
    """
    if not api_key or OpenAI is None:
        return None, None

    try:
        client = OpenAI(api_key=api_key)
        emo_summary = ", ".join(f"{k}: {v:.2f}" for k, v in emotion_scores.items())
        prompt = (
            "You are an AI artist. Create a very short, poetic title and a one-sentence "
            "caption for a generative dream aura poster.\n\n"
            f"Dream text: {dream_text}\n"
            f"Emotional profile (0-1): {emo_summary}\n\n"
            "Return your answer in the following format:\n"
            "Title: <short title>\n"
            "Caption: <one sentence, max 25 words>"
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
            max_tokens=120,
        )
        content = response.choices[0].message.content.strip()

        title = None
        caption = None
        for line in content.splitlines():
            line = line.strip()
            if line.lower().startswith("title:"):
                title = line.split(":", 1)[1].strip()
            elif line.lower().startswith("caption:"):
                caption = line.split(":", 1)[1].strip()
        return title, caption
    except Exception:
        # If anything goes wrong, just fall back to heuristic version
        return None, None


def main():
    st.set_page_config(
        page_title="Aura Tarot Dream Analyzer",
        page_icon="💫",
        layout="wide",
    )

    # ----------------- HEADER -----------------
    st.title("💫 Aura Tarot Dream Analyzer")
    st.write(
        "Turn your dream into **symbols, emotional data, aura colors,** "
        "a **generative art poster**, and a gentle **tarot-style reflection**."
    )

    # ----------------- SIDEBAR -----------------
    with st.sidebar:
        st.header("Dream Settings")

        aura_style = st.selectbox(
            "Aura style",
            ["Mystic", "Pastel", "Cyber", "Golden"],
            index=0,
        )

        poster_complexity = st.slider(
            "Poster complexity",
            min_value=0.6,
            max_value=1.6,
            value=1.0,
            step=0.1,
            help="Controls how many layers / blobs the aura poster will use.",
        )

        st.markdown("---")
        st.subheader("OpenAI (optional)")
        api_key = st.text_input(
            "Your OpenAI API key",
            type="password",
            help="If provided, the app will generate a poetic aura title & caption.",
        )
        st.caption(
            "Core analysis runs locally. The OpenAI key is only used to enhance "
            "the title/caption and is **optional**."
        )

    # ----------------- STEP 1: DREAM INPUT -----------------
    st.markdown("### 1. Enter dream text")
    dream_text = st.text_area(
        "Describe your dream in 3–10 sentences.",
        height=220,
        placeholder=(
            "Example: I was running in a dark train station, wearing a white dress. "
            "The sea was below the bridge and I was afraid of falling..."
        ),
    )

    analyze_clicked = st.button("✨ Analyze Dream & Generate Aura")

    if not analyze_clicked:
        st.info(
            "Write your dream above and click **“✨ Analyze Dream & Generate Aura”**.\n\n"
            "The app will then:\n"
            "1. Parse key dream symbols\n"
            "2. Compute six emotional factors\n"
            "3. Visualize a radar chart & aura bar\n"
            "4. Generate an abstract aura poster\n"
            "5. Provide tarot-style interpretation text"
        )
        return

    if not dream_text.strip():
        st.warning("Please write something about your dream first.")
        return

    # ================= ANALYSIS LAYERS =================
    # Layer 1: symbols
    symbols = analyze_symbols(dream_text)
    # Layer 2: six emotional factors
    emotion_scores = extract_emotions(dream_text)
    # Optional OpenAI aura title / caption
    aura_title, aura_caption = generate_openai_aura_title(api_key, dream_text, emotion_scores)

    # --------- TABS: like classmates' rich dashboards ---------
    tab_overview, tab_data, tab_poster = st.tabs(
        ["🌙 Overview", "📊 Emotional Data & Aura", "🎨 Poster & Tarot"]
    )

    # ----------------- TAB 1: OVERVIEW -----------------
    with tab_overview:
        st.subheader("Layer 1 — Symbolic interpretation (What you saw)")
        if symbols:
            st.write("Detected symbols and short meanings:")
            for s in symbols:
                explanation = SYMBOLS.get(s, "")
                st.markdown(f"- **{s.capitalize()}** — {explanation}")
        else:
            st.write(
                "No predefined symbols were matched, but your dream will still be "
                "interpreted through emotional pattern and aura art."
            )

        st.markdown("---")
        st.subheader("Dream aura summary")
        if aura_title:
            st.markdown(f"**OpenAI Aura Title:** {aura_title}")
            if aura_caption:
                st.caption(aura_caption)
        else:
            st.write(
                "Aura title: *A field of colors shaped by your emotional profile.*  \n"
                "You can add an OpenAI API key in the sidebar to get a custom poetic title."
            )

    # ----------------- TAB 2: DATA & AURA -----------------
    with tab_data:
        st.subheader("Layer 2 — Six emotional factors (What you felt)")

        cols = st.columns(len(EMOTIONS))
        for col, emo in zip(cols, EMOTIONS):
            with col:
                st.metric(emo, f"{emotion_scores[emo]:.2f}")

        st.markdown("#### Emotion radar chart")
        radar_fig = create_radar_chart(emotion_scores)
        st.pyplot(radar_fig, use_container_width=True)

        st.markdown("#### Aura energy bar (color spectrum)")
        aura_fig = create_aura_bar(emotion_scores, aura_style)
        st.pyplot(aura_fig, use_container_width=True)

    # ----------------- TAB 3: POSTER & TAROT -----------------
    with tab_poster:
        st.subheader("Layer 3 — Generative Aura Poster (Emotional DNA)")

        # poster_complexity 影响图层数量，让不同梦境更明显
        scaled_scores = {k: v * poster_complexity for k, v in emotion_scores.items()}
        poster_fig = create_aura_poster(scaled_scores, aura_style)
        st.pyplot(poster_fig, use_container_width=True)

        # Download button
        buf = BytesIO()
        poster_fig.savefig(buf, format="png", dpi=300, bbox_inches="tight")
        buf.seek(0)
        st.download_button(
            label="📥 Download Aura Poster (PNG)",
            data=buf,
            file_name="aura_dream_poster.png",
            mime="image/png",
        )

        st.markdown("---")
        st.subheader("Layer 4 — Tarot-style interpretation (What it means)")
        shadow, energy, guidance = generate_tarot_reading(symbols, emotion_scores)

        st.markdown("**Shadow — subconscious message**")
        st.write(shadow)

        st.markdown("**Energy — current emotional flow**")
        st.write(energy)

        st.markdown("**Guidance — supportive insight**")
        st.write(guidance)

        st.caption("Dream → Meaning → Data → Art → Guidance")


if __name__ == "__main__":
    main()
