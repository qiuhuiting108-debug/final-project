import streamlit as st
from src.generator import generate_abstract_art

st.set_page_config(page_title="Dream Visualizer", layout="wide")

st.title("✨ Dream Visualizer — Abstract AI Poster Generator")

st.write("Describe your dream, and the AI will transform it into an abstract generative poster.")

# -----------------------------
# 1. Dream input
# -----------------------------
dream_text = st.text_area("📝 Enter your dream description:", height=150)

# Style options
style = st.selectbox(
    "🎨 Choose poster style",
    ["Energy Waves", "Emotional Bloom", "Cosmic Spiral", "Chaos Flow", "Neon Aura"]
)

generate_btn = st.button("Generate Poster")

# -----------------------------
# 2. Generate when button clicked
# -----------------------------
if generate_btn:
    if not dream_text.strip():
        st.error("Please enter your dream description.")
    else:
        with st.spinner("🎨 Generating your personalized poster..."):
            fig = generate_abstract_art(dream_text, style)
            st.pyplot(fig)
