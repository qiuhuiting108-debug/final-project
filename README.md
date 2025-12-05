# 🌙 Aura Tarot Dream Analyzer  
**All-in-One Final Project for “Arts & Advanced Big Data”**  
**Author:** Huiting Qiu (邱慧婷)

---

## ⭐ Overview  
**Aura Tarot Dream Analyzer** is an AI-powered interactive system that transforms a user's dream into:

1. **A symbolic interpretation** (via OpenAI or fallback rule-based model)  
2. **A structured 6-dimensional emotional dataset**  
3. **Data visualizations** (Radar Chart + Aura Spectrum Bar)  
4. **Hybrid generative art posters** blending  
   - geometric styles inspired by class examples  
   - aura-style abstract diffusion fields  
5. **Tarot-inspired insights** summarizing the dream’s subconscious energy  

This project integrates **AI, data-driven modeling, visualization, and generative art**—synthesizing major components learned throughout the semester into a single cohesive experience.

---

## 🎯 Goal  
The goal of this project is to build an interactive AI system that helps users *understand their dreams and visualize their emotional state*. The system transforms a dream description into:

- a **structured interpretation of symbols and themes**,  
- **visualized emotional data** through charts and aura spectrums,  
- and a **generative abstract poster** guided by the emotions extracted from the dream.

By combining AI text analysis, emotional modeling, generative art, and interactive visualization, this project aims to turn inner psychological experiences into meaningful, aesthetically engaging visual artifacts.

---

## ✨ Key Features  

### 1. AI Dream Interpretation  
- Uses the OpenAI Responses API (`gpt-4.1-mini`) when `OPENAI_API_KEY` is available.  
- Returns structured JSON containing:  
  - `symbolic_summary`  
  - `emotions` (Fear, Desire, Calm, Mystery, Connection, Transformation)  
  - `tarot_shadow`, `tarot_energy`, `tarot_guidance`  
- If no API key is set, the app falls back to a transparent rule-based emotion model.

### 2. 6-Dimensional Emotion Modeling  
Each dream is converted into a six-dimensional emotional vector:

- **Fear**  
- **Desire**  
- **Calm**  
- **Mystery**  
- **Connection**  
- **Transformation**  

All emotion values are scaled within `[0.0–1.0]` and used to drive both visualization and generative art parameters.

### 3. Data Visualization  
- **Radar Chart** to display the emotional distribution.  
- **Aura Energy Spectrum Bar** to show the relative strength of each emotional dimension as color bands.

### 4. Hybrid Generative Poster Engine  
Two-layer generative art system:

- **Aura Layer**  
  - Smooth 2D field using radial distance, exponential decay, and wave interference.  
  - Colors encoded by warm/cool channels and transformation brightness.

- **Geometric Layer**  
  - Grid of rectangles with random jitter, opacity, and size.  
  - Number of cells and density influenced by transformation and calm.

Three visual modes:

- **Hybrid** – balanced aura + geometry  
- **Geometric Focus** – stronger geometric grid, lighter aura  
- **Aura Focus** – strong aura field, minimal geometry  

### 5. Tarot-Inspired Interpretation  
The system produces:

- **Shadow** – subconscious message behind the dream  
- **Energy** – current aura energy based on emotions  
- **Guidance** – gentle, non-fatalistic advice  

This blends psychological reflection with symbolic, tarot-like language.

### 6. Interactive Streamlit Web App  
- Dream text input  
- Poster style selection (Hybrid / Geometric Focus / Aura Focus)  
- Option to generate two poster variations  
- Real-time display of:  
  - symbolic summary  
  - tarot reading  
  - radar chart  
  - aura spectrum  
  - hybrid generative posters  
- Download buttons for poster PNG files

---

## 🧠 System Architecture  

```text
                      +------------------------+
                      |  User Dream Text Input |
                      +-----------+------------+
                                  |
                                  v
                   +-------------------------------+
                   |  AI Dream Analysis (OpenAI)   |
                   |  or Rule-based Fallback       |
                   +-------------------------------+
                                  |
                 +----------------+----------------+
                 |                                 |
                 v                                 v
     +-------------------+              +------------------------+
     | Emotion Data (6D) |              | Symbolic & Tarot Text |
     +--------+----------+              +-----------+------------+
              |                                     |
              v                                     v
 +---------------------------+         +----------------------------+
 | Radar Chart Visualization |         | Aura Spectrum Visualization|
 +-------------+-------------+         +-------------+--------------+
               |                                       |
               v                                       |
      +------------------------+                       |
      | Hybrid Poster Generator|<----------------------+
      +-----------+------------+
                  |
                  v
      +---------------------------+
      | Poster Output (PNG)       |
      +---------------------------+
