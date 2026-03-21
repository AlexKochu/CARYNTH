# Career Architect – Technical Implementation Report

## 1. Executive Summary
**Career Architect** is an intelligent, end-to-end Student Career Recommendation System. It leverages a hybrid machine learning approach (Classification + Clustering) enhanced by an NLP normalization layer to predict optimal job roles, identify skill gaps, and generate personalized learning roadmaps. The system is deployed via a high-performance FastAPI backend and served through a modern, corporate-grade dashboard.

---

## 2. System Inventory: What Was Created

### A. Core Codebase
1.  **`train_models.py` (Model Engine)**
    -   **Purpose**: Orchestrates the data loading, preprocessing, model training, and serialization pipeline.
    -   **Outputs**: Generates the 5 critical `.pkl` artifacts required for inference.

2.  **`main.py` (Inference Backend)**
    -   **Framework**: FastAPI (Python).
    -   **Purpose**: Exposes the AI logic via REST endpoints. Handles model loading, NLP normalization, affinity scoring, and dynamic path generation.

3.  **Frontend Suite (`index.html`, `style.css`, `script.js`)**
    -   **Purpose**: A single-page application (SPA) dashboard.
    -   **Design**: Dark-mode corporate UI with animated SVG gauges, vertical roadmaps, and modular result cards. No page reloads (AJAX/Fetch flow).

### B. Serialized Models (Pickle Files)
| File | Algorithm | Purpose |
| :--- | :--- | :--- |
| `career_rf_model.pkl` | **Random Forest Classifier** | Predicts the target Job Role based on complex feature interactions. |
| `career_cluster_model.pkl` | **K-Means Clustering** | Groups students into peer clusters (e.g., "Cluster 2") for comparative insights. |
| `skill_vectorizer.pkl` | **CountVectorizer** | Converts text skills into a sparse numerical matrix for the ML models. |
| `interest_encoder.pkl` | **LabelEncoder** | Encodes categorical interest areas into numerical format. |
| `role_encoder.pkl` | **LabelEncoder** | Decodes model predictions back into human-readable job titles. |

### C. API Specification
-   **Endpoint**: `POST /predict`
-   **Input**: JSON payload containing `cgpa`, `interest`, `skills`, `courses_completed`, `projects_count`.
-   **Output**: JSON response with `predicted_role`, `cluster_id`, `skill_gap` (list), `learning_path` (list), and `career_score` (float).

---

## 3. Transformations: What Was Changed & Improved

### A. ML Pipeline Modifications
*Original Approach*: Simple mapping or basic training.
*New Approach*: **Robust Hybrid Pipeline**.
1.  **Retraining Strategy**: Instead of relying on potentially corrupt or mismatched `.pkl` files, I implemented a fresh retraining script (`train_models.py`) that strictly aligns feature inputs (Skill Vectors + Scalars) to ensure 100% compatibility between training and inference phases.
2.  **Feature Expansion**: The skill vectorizer was integrated into the main feature set (`np.hstack`), combining sparse text data with dense numerical data (CGPA) for a holistic prediction model.

### B. NLP & Logic Enhancements (The "Additions")

#### 1. NLP Skill Normalization Layer (New)
*Problem*: Users enter "ReactJS", "React.js", or "react". Models treat these as different features.
*Solution*: Implemented a **Canonical Ontology** in `main.py`.
*Mechanism*:
-   **Pre-processor**: Lowercases, removes special chars (`react.js` -> `reactjs`).
-   **Ontology Map**: Maps synonyms to a single key (e.g., `["nn", "deep learning"]` -> `neuralnetworks`).
*Benefit*: "Torch" and "PyTorch" are now mathematically identical, preventing false negatives in skill gap detection.

#### 2. Scientific Readiness Scoring (New)
*Problem*: Original logic was a simple count. One skill could yield a 50% score.
*Solution*: **Weighted Role-Based Logic**.
-   Defined expert weight maps (e.g., Data Scientist: Python=25%, Stats=20%, SQL=10%).
-   Readiness Score = $\sum (MatchedSkillWeight * 80) + (CGPA * 10) + (Projects * 10)$
-   **Critical Dampening**: If matching skills contribution is < 10%, total score is capped at 15% even if CGPA is high. This ensures the score reflects *employability*, not just academic grades.

#### 3. Dynamic Learning Roadmap (New)
*Problem*: Static suggestions.
*Solution*: Algorithmically generated path.
-   Step 1: Identify specific missing canonical skills.
-   Step 2: Generate "Learn X Fundamentals" for top 3 gaps.
-   Step 3: Append "Master remaining skills for [Role]" if gaps remain.

---

## 4. Technical Justification (The "Why")

| Feature | Problem it Solves | Technical Justification |
| :--- | :--- | :--- |
| **NLP Normalization** | "Skill Mismatch" due to spelling/synonyms. | Reduces dimensionality and sparsity. Increases model robustness to real-world noisy input. Essential for User Experience. |
| **Weighted Scoring** | "Inflation" of competence scores. | A linear count doesn't reflect the *importance* of a skill. Weighted sums align with industry hiring standards (Core vs. Nice-to-have). |
| **FastAPI Backend** | Static execution limitations. | Enables asynchronous handling, type validation (Pydantic), and easy decoupling of Frontend/Backend for scalable deployment. |
| **Corporate UI** | "Student Project" look & feel. | Transforms the project into a viable product demo. Dark mode and animations imply sophistication and high production value. |

---

## 5. End-to-End Architecture Flow

1.  **User Input**: Student enters data in the Dashboard.
    *   *Input*: "NeuralNetworks, torch", CGPA: 8.5
2.  **Transmission**: JS `fetch()` sends JSON payload to `POST /predict`.
3.  **Layer 1 - Normalization (NLP)**:
    *   Backend intercepts skills.
    *   "NeuralNetworks" -> `neuralnetworks`
    *   "torch" -> `pytorch`
4.  **Layer 2 - Encoding**:
    *   `neuralnetworks` + `pytorch` -> Vectorized to `[0, 1, ... 1]` via `CountVectorizer`.
    *   Interest "AI" -> Encoded to `0` via `LabelEncoder`.
5.  **Layer 3 - Inference**:
    *   **Classification**: Random Forest receives combined vector -> Predicts "AI/ML Engineer".
    *   **Clustering**: KMeans receives vector -> Assigns "Cluster 2" (High achievers).
6.  **Layer 4 - Post-Processing**:
    *   **Gap Analysis**: Compares User Norm Skills vs. Role Norm Skills.
    *   **Scoring**: Applies weighted formula.
    *   **Roadmap**: Generates steps.
7.  **Response**: JSON sent back to frontend.
8.  **Visualization**: Dashboard renders Gauge, Tags, and Timeline.

---

## 6. Conclusion
This project has evolved from a basic prediction script into a **Deployment-Ready AI System**. The addition of the NLP layer and weighted scoring model specifically addresses the gap between academic prototypes and real-world application requirements, ensuring that the system is not just "working," but **accurate, robust, and user-friendly**.
