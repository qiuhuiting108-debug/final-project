# src/analyzer.py

from typing import Dict, List


# Dream symbols and their short explanations (Layer 1)
SYMBOLS: Dict[str, str] = {
    "water": "Water → emotional depth, instability, or changing feelings.",
    "sea": "Sea → vast emotions and the unknown parts of yourself.",
    "ocean": "Ocean → powerful, overwhelming emotions or life changes.",
    "river": "River → the flow of time, relationships, or life direction.",
    "drown": "Drowning → feeling overwhelmed or out of control emotionally.",
    "fire": "Fire → passion, anger, or intense transformation.",
    "bridge": "Bridge → transition, crossing from one stage to another.",
    "fall": "Falling → loss of control, insecurity, or fear of failure.",
    "train": "Train → pressure, life rhythm, or a set direction you are following.",
    "station": "Station → waiting, choices, or preparation for change.",
    "stranger": "Stranger → unknown self, new sides of your personality.",
    "dark": "Darkness → uncertainty, hidden fears, or confusion.",
    "light": "Light → awareness, realization, or hope.",
    "white dress": "White dress → purity, expectation, or social roles about identity.",
    "door": "Door → opportunity, boundary, or a choice you may need to make.",
    "corridor": "Corridor → transition zone, searching for direction.",
    "chase": "Being chased → avoiding problems or pressure.",
    "exam": "Exam → self-judgement, pressure to prove your value.",
    "family": "Family → core relationships, support, or unresolved family issues.",
    "friend": "Friends → social connection, support, or comparison.",
    "lover": "Lover → intimacy, expectations in relationships, or emotional needs.",
    "kiss": "Kiss → desire for connection, acceptance, or emotional closeness.",
    "death": "Death → ending of a phase, transformation, or deep change.",
    "reborn": "Rebirth → healing, new beginning, and inner growth.",
    "flying": "Flying → freedom, gaining perspective, or escaping limits.",
}


def analyze_symbols(text: str) -> List[str]:
    """
    Detect known symbols in the dream text (order preserved, no duplicates).
    """
    text_lower = text.lower()
    found: List[str] = []

    # Handle multi-word symbols first
    if "white dress" in text_lower:
        found.append("white dress")

    for key in SYMBOLS.keys():
        if key == "white dress":
            continue
        if key in text_lower:
            found.append(key)

    # Deduplicate while preserving order
    seen = set()
    ordered: List[str] = []
    for symbol in found:
        if symbol not in seen:
            ordered.append(symbol)
            seen.add(symbol)
    return ordered


def generate_tarot_reading(symbols, emotion_scores):
    """
    Generate a three-part tarot-style reading:
    Shadow / Energy / Guidance.
    """
    # Dominant emotions
    sorted_emotions = sorted(
        emotion_scores.items(), key=lambda x: x[1], reverse=True
    )
    dom1, dom2 = sorted_emotions[0][0], sorted_emotions[1][0]

    aura_map = {
        "Fear": "deep blue and indigo tones, showing hidden worries and tension",
        "Desire": "rose and red aura, reflecting strong longing and emotional intensity",
        "Calm": "soft green and blue fields, suggesting recovery and emotional healing",
        "Mystery": "violet twilight light, symbolizing intuition and unanswered questions",
        "Connection": "warm orange glow, expressing relationships and emotional bonds",
        "Transformation": "golden light, hinting at change, ending, and new beginnings",
    }
    aura_sentence = aura_map.get(
        dom1, "shifting colors that mirror your complex emotions."
    )

    # Shadow
    shadow_parts = []
    if symbols:
        important = symbols[:3]
        shadow_parts.append(
            "In your dream, symbols like "
            + ", ".join(important)
            + " appear. They point to themes you may not fully face yet."
        )

    if emotion_scores.get("Fear", 0) > 0.55 or emotion_scores.get("Mystery", 0) > 0.55:
        shadow_parts.append(
            "There is a strong undercurrent of fear or uncertainty, "
            "suggesting you might be avoiding a conversation, decision, or emotion in waking life."
        )
    else:
        shadow_parts.append(
            "The shadow side of this dream is gentle — it hints at subtle doubts rather than overwhelming fear."
        )
    shadow_text = " ".join(shadow_parts)

    # Energy
    energy_text = (
        f"Your aura leans toward {aura_sentence}. "
        f"The main energies in this dream are **{dom1}** and **{dom2}**, "
        f"shaping how you react and move right now."
    )

    # Guidance
    guidance_parts = []
    if emotion_scores.get("Transformation", 0) >= 0.5:
        guidance_parts.append(
            "This is a transition moment. Let old expectations slowly fall away, "
            "and allow yourself to step into a new rhythm."
        )
    if emotion_scores.get("Calm", 0) >= 0.5:
        guidance_parts.append(
            "Even if the dream feels intense, there is a calm core inside you. "
            "Trust that you are already learning how to balance your emotions."
        )
    if emotion_scores.get("Connection", 0) >= 0.5:
        guidance_parts.append(
            "Reach out to people you trust — sharing what you feel can turn isolation into support."
        )
    if not guidance_parts:
        guidance_parts.append(
            "Take one small, kind action for yourself today — a walk, a note, or a quiet moment. "
            "Small rituals can gently realign your energy."
        )
    guidance_text = " ".join(guidance_parts)

    return shadow_text, energy_text, guidance_text
