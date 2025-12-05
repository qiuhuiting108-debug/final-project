"""
analyzer.py

High-level dream analyzer that:
- Tries to use the OpenAI Responses API for rich analysis.
- Falls back to a rule-based emotion model if the API is unavailable.

It returns a unified result dict and a string describing
which model was used, so the UI can display this clearly.
"""

import os
import json
from typing import Tuple, Dict, Any, Optional

from openai import OpenAI
from .emotion_model import rule_based_emotion_model

SYSTEM_INSTRUCTIONS = """
You are a dream analysis assistant for an art-and-data project.

Your task:
Given a short dream description, you must output ONLY a valid JSON object
with the following structure:

{
  "symbolic_summary": "2-4 sentences explaining the main symbols and themes in the dream.",
  "emotions": {
    "Fear": 0.0-1.0,
    "Desire": 0.0-1.0,
    "Calm": 0.0-1.0,
    "Mystery": 0.0-1.0,
    "Connection": 0.0-1.0,
    "Transformation": 0.0-1.0
  },
  "tarot_shadow": "2-4 sentences describing the subconscious message of the dream.",
  "tarot_energy": "1-3 sentences describing the current aura energy.",
  "tarot_guidance": "1-3 sentences giving gentle, non-fatalistic advice."
}

Rules:
- All emotion values must be floating-point numbers between 0.0 and 1.0.
- Make sure the JSON is syntactically valid (no trailing commas, no comments).
- Do NOT include any explanation outside the JSON. Output ONLY JSON.
- Tone: reflective, supportive, slightly poetic but still clear.
"""


def get_openai_client() -> Optional[OpenAI]:
    """
    Initialize an OpenAI client using the OPENAI_API_KEY
    environment variable. Returns None if no key is set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def _analyze_dream_with_openai(client: OpenAI, dream_text: str) -> Optional[Dict[str, Any]]:
    """
    Internal helper: call OpenAI Responses API and parse JSON.
    Returns a dict or None if something goes wrong.
    """
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "developer", "content": SYSTEM_INSTRUCTIONS},
                {"role": "user", "content": dream_text},
            ],
            max_output_tokens=600,
        )

        raw_text = response.output_text
        data = json.loads(raw_text)

        if "emotions" not in data:
            return None

        required_keys = [
            "Fear", "Desire", "Calm",
            "Mystery", "Connection", "Transformation"
        ]
        for key in required_keys:
            if key not in data["emotions"]:
                return None

        return data

    except Exception as e:
        # In this course project we just print the error and fall back.
        print("OpenAI error:", e)
        return None


def analyze_dream(dream_text: str) -> Tuple[Dict[str, Any], str]:
    """
    Unified dream analysis entry point.

    Returns:
        result_dict, model_name_used
    """
    client = get_openai_client()
    if client is not None:
        data = _analyze_dream_with_openai(client, dream_text)
        if data is not None:
            return data, "OpenAI gpt-4.1-mini (Responses API)"

    # Fallback
    fallback_data = rule_based_emotion_model(dream_text)
    return fallback_data, "Rule-based fallback model"
