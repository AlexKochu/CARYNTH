```
   ██████╗ █████╗ ██████╗ ██╗   ██╗███╗   ██╗████████╗██╗  ██╗
  ██╔════╝██╔══██╗██╔══██╗╚██╗ ██╔╝████╗  ██║╚══██╔══╝██║  ██║
  ██║     ███████║██████╔╝ ╚████╔╝ ██╔██╗ ██║   ██║   ███████║
  ██║     ██╔══██║██╔══██╗  ╚██╔╝  ██║╚██╗██║   ██║   ██╔══██║
  ╚██████╗██║  ██║██║  ██║   ██║   ██║ ╚████║   ██║   ██║  ██║
   ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
```

<h1 align="center">CARYNTH — AI-Powered Career Architect</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=flat-square&logo=fastapi" />
  <img src="https://img.shields.io/badge/scikit--learn-ML%20Engine-F7931E?style=flat-square&logo=scikitlearn" />
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
</p>

---

## Overview

CARYNTH is an AI-powered Career Recommendation Engine that leverages a **Hybrid Random Forest + K-Means clustering algorithm** to analyze a user's academic attributes and technical skill profile. It predicts optimal tech career roles, surfaces actionable skill gaps, and generates a personalized, strategic learning roadmap — built for students and early-career professionals navigating the modern technology landscape.

---

## Key Capabilities

| Capability                  | Description                                                                 |
|-----------------------------|-----------------------------------------------------------------------------|
| [>] Role Prediction         | Classifies ideal tech roles from academic and skill data via Random Forest  |
| [~] Skill Gap Analysis      | Identifies missing competencies against target-role benchmarks              |
| [*] NLP Vectorization       | Transforms free-form skill input into structured ML-compatible feature sets |
| [+] Roadmap Generation      | Produces a sequenced, milestone-based personal learning plan                |
| [#] Cluster Profiling       | Groups similar user profiles via K-Means for cohort-level insights          |

---

## Architecture

CARYNTH is organized into two decoupled layers that communicate over a REST API:

```
  ┌─────────────────────────────────────────────────────────────┐
  │                        CARYNTH SYSTEM                       │
  │                                                             │
  │   ┌──────────────────────┐     ┌──────────────────────┐    │
  │   │      FRONTEND        │     │       BACKEND         │    │
  │   │  ─────────────────   │     │  ─────────────────    │    │
  │   │  HTML / CSS / JS     │────▶│  FastAPI + Uvicorn    │    │
  │   │  Single-Page App     │     │  ML Inference Engine  │    │
  │   │  Scroll Animations   │◀────│  NLP Vectorizer       │    │
  │   │  Inline Results      │     │  Scoring & Ranking    │    │
  │   └──────────────────────┘     └──────────────────────┘    │
  │                                          │                  │
  │                              ┌───────────▼───────────┐      │
  │                              │     ML MODEL LAYER    │      │
  │                              │  ─────────────────    │      │
  │                              │  Random Forest (.pkl) │      │
  │                              │  K-Means (.pkl)       │      │
  │                              │  TF-IDF Encoder (.pkl)│      │
  │                              │  Label Encoder (.pkl) │      │
  │                              └───────────────────────┘      │
  └─────────────────────────────────────────────────────────────┘
```

---

## System Flow

```
  USER INPUT
      │
      │  Academic scores, GPA, skills, interests
      ▼
  ┌────────────────────┐
  │   Frontend SPA     │  ── Collects & validates user profile
  └────────┬───────────┘
           │  POST /predict
           ▼
  ┌────────────────────┐
  │  FastAPI Backend   │  ── Receives and parses JSON payload
  └────────┬───────────┘
           │
           ▼
  ┌────────────────────┐
  │  NLP Vectorizer    │  ── Transforms skill strings → feature vectors
  └────────┬───────────┘
           │
           ▼
  ┌──────────────────────────────────────────┐
  │              Inference Layer             │
  │                                          │
  │  ┌──────────────┐   ┌────────────────┐  │
  │  │ Random Forest│   │  K-Means Model │  │
  │  │  Classifier  │   │ Cluster Assign │  │
  │  └──────┬───────┘   └───────┬────────┘  │
  │         │                   │            │
  │         └─────────┬─────────┘            │
  │                   ▼                      │
  │         ┌─────────────────┐              │
  │         │ Scoring Engine  │              │
  │         │ Gap Analyzer    │              │
  │         └────────┬────────┘              │
  └──────────────────┼───────────────────────┘
                     │
                     ▼
  ┌────────────────────┐
  │  JSON Response     │  ── Role, gaps, roadmap, confidence scores
  └────────┬───────────┘
           │
           ▼
  ┌────────────────────┐
  │  Frontend Renderer │  ── Inline display, no page reload
  └────────────────────┘
           │
           ▼
      USER DASHBOARD
      Predicted Role · Skill Gaps · Learning Roadmap
```

---

## Project Structure

```
  CARYNTH/
  │
  ├── frontend/                        # [>] UI/UX Interface Layer
  │   ├── index.html                   #     Main single-page application layout
  │   ├── style.css                    #     Premium styling, animations, themes
  │   └── script.js                    #     API integration & interaction logic
  │
  ├── backend/                         # [*] AI & API Engine
  │   ├── main.py                      #     FastAPI server, route definitions, CORS
  │   ├── train_models.py              #     ML training pipeline (RF + K-Means)
  │   ├── student_career_data.csv      #     Source dataset for model training
  │   ├── random_forest_model.pkl      #     Serialized Random Forest classifier
  │   ├── kmeans_model.pkl             #     Serialized K-Means cluster model
  │   ├── tfidf_vectorizer.pkl         #     TF-IDF NLP skill encoder
  │   └── label_encoder.pkl            #     Target label encoder for role classes
  │
  └── docs/                            # [#] Technical Documentation
      ├── architecture.md              #     System design & component overview
      ├── nlp_vectorization.md         #     NLP pipeline & skill encoding guide
      └── model_architecture.md        #     Random Forest & K-Means deep-dive
```

---

## Getting Started

### Prerequisites

Ensure the following are available on your system before proceeding:

```
  [✓] Python 3.8 or higher
  [✓] pip (Python package installer)
  [✓] A modern web browser (Chrome, Firefox, Edge)
  [ ] VS Code + Live Server extension (optional, recommended)
```

---

### Step 1 — Backend Setup

Navigate to the backend directory and install all required dependencies:

```bash
  cd backend
```

```bash
  pip install fastapi uvicorn pydantic scikit-learn numpy pandas
```

Start the FastAPI inference server with hot-reload enabled:

```bash
  uvicorn main:app --reload
```

The AI engine will be live at:

```
  http://127.0.0.1:8000
  http://127.0.0.1:8000/docs      ← Interactive Swagger UI
  http://127.0.0.1:8000/redoc     ← ReDoc API Reference
```

---

### Step 2 — Model Training (First Run Only)

If the `.pkl` model files are not present, train the models against the included dataset:

```bash
  python train_models.py
```

This will generate the following serialized artifacts in the `backend/` directory:

```
  backend/
  ├── random_forest_model.pkl
  ├── kmeans_model.pkl
  ├── tfidf_vectorizer.pkl
  └── label_encoder.pkl
```

> Note: Pre-trained model files are included in the repository. Re-training is only necessary if you modify the dataset or wish to retune hyperparameters.

---

### Step 3 — Frontend Setup

Navigate to the `frontend/` directory and open the application:

**Option A — Direct File Open**

```
  Double-click  frontend/index.html
```

**Option B — VS Code Live Server (Recommended)**

```
  1. Open the project root in VS Code
  2. Right-click frontend/index.html
  3. Select "Open with Live Server"
  4. Application will hot-reload at http://127.0.0.1:5500
```

> Ensure the backend is running before launching the frontend. The frontend makes live API calls to `http://127.0.0.1:8000`.

---

## API Reference

### POST `/predict`

Accepts a user profile and returns role predictions, skill gaps, and a learning roadmap.

**Request Body**

```json
  {
    "gpa": 3.7,
    "academic_scores": {
      "mathematics": 88,
      "data_structures": 92,
      "databases": 75
    },
    "skills": ["Python", "SQL", "Machine Learning", "Git"]
  }
```

**Response**

```json
  {
    "predicted_role": "Data Scientist",
    "confidence": 0.91,
    "cluster_id": 3,
    "skill_gaps": ["Cloud Platforms", "Deep Learning", "MLOps"],
    "roadmap": [
      { "step": 1, "topic": "Cloud Fundamentals (AWS/GCP)", "duration": "3 weeks" },
      { "step": 2, "topic": "Deep Learning with TensorFlow", "duration": "6 weeks" },
      { "step": 3, "topic": "MLOps & Model Deployment", "duration": "4 weeks" }
    ]
  }
```

### GET `/health`

Returns server and model availability status.

```json
  { "status": "ok", "models_loaded": true }
```

---

## ML Model Overview

```
  ┌────────────────────────────────────────────────────────────┐
  │                    TRAINING PIPELINE                       │
  │                                                            │
  │   student_career_data.csv                                  │
  │          │                                                 │
  │          ▼                                                 │
  │   ┌─────────────────┐                                      │
  │   │  Preprocessing  │  ── Normalize, encode, vectorize     │
  │   └───────┬─────────┘                                      │
  │           │                                                │
  │    ┌──────┴──────┐                                         │
  │    ▼             ▼                                         │
  │  ┌─────────┐  ┌────────┐                                   │
  │  │   RF    │  │K-Means │  ── Parallel training             │
  │  │Classifier│ │Cluster │                                   │
  │  └────┬────┘  └───┬────┘                                   │
  │       │           │                                        │
  │       ▼           ▼                                        │
  │   Serialize → .pkl artifacts                               │
  └────────────────────────────────────────────────────────────┘
```

| Model          | Type                   | Purpose                              |
|----------------|------------------------|--------------------------------------|
| Random Forest  | Supervised Classifier  | Role prediction with confidence score|
| K-Means        | Unsupervised Clustering| User cohort and profile grouping     |
| TF-IDF         | NLP Vectorizer         | Skill string → numeric feature map   |
| Label Encoder  | Transformer            | Encodes/decodes career role classes  |

---

## Tech Stack

```
  ┌─────────────────┬─────────────────────────────────────────┐
  │ Layer           │ Technology                              │
  ├─────────────────┼─────────────────────────────────────────┤
  │ Frontend        │ HTML5, CSS3, Vanilla JavaScript         │
  │ Backend         │ Python 3.8+, FastAPI, Uvicorn           │
  │ ML Framework    │ scikit-learn (RF, K-Means, TF-IDF)      │
  │ Data Processing │ pandas, NumPy                           │
  │ Serialization   │ pickle (.pkl model artifacts)           │
  │ API Format      │ REST / JSON                             │
  └─────────────────┴─────────────────────────────────────────┘
```

---

## Documentation

Detailed technical documentation is located in the `docs/` directory:

```
  docs/
  ├── architecture.md          System design and component overview
  ├── nlp_vectorization.md     NLP pipeline and TF-IDF skill encoding
  └── model_architecture.md   Random Forest and K-Means deep-dive
```

---

## Contributing

Contributions are welcome. Please follow the standard fork-and-PR workflow:

```
  1. Fork the repository
  2. Create a feature branch     git checkout -b feature/your-feature
  3. Commit your changes         git commit -m "feat: describe your change"
  4. Push to your branch         git push origin feature/your-feature
  5. Open a Pull Request
```

---

## License

This project is licensed under the **MIT License**. See `LICENSE` for full terms.

---

<p align="center">
  Built with precision — CARYNTH &copy; 2025
</p>