# -----------------------------------
# 3. Posters (Dream-dependent seed)
# -----------------------------------

import hashlib

def dream_to_seed(text: str) -> int:
    """Generate deterministic seed from dream text"""
    h = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return int(h[:8], 16)

if analyze_button:

    st.subheader("4. Generative Aura Posters")

    # 1) Convert dream text → deterministic seed
    seed_base = dream_to_seed(dream_text)

    # 2) Poster Variation 1
    poster_fig_1 = generate_hybrid_poster(
        emotions,
        style=poster_style,
        seed=seed_base,        # dream-specific seed
    )

    st.markdown("### **Poster Variation 1**")
    st.pyplot(poster_fig_1, use_container_width=True)

    # 3) Poster Variation 2 (optional)
    poster_fig_2 = None
    if multi_variation:
        poster_fig_2 = generate_hybrid_poster(
            emotions,
            style=poster_style,
            seed=seed_base + 37,    # second variation seed
        )

        st.markdown("### **Poster Variation 2**")
        st.pyplot(poster_fig_2, use_container_width=True)

    st.success("Posters generated using dream-dependent random seeds.")
