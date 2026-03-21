# CARYNTH: AI-Powered Career Architect

CARYNTH is an advanced AI Career Recommendation Engine that utilizes a Hybrid Random Forest and KMeans algorithm to analyze academic attributes and technical skills. It predicts ideal tech roles, identifies skill gaps, and generates a personalized, strategic learning roadmap for students and professionals.

## Architecture

The project is structured cleanly into two main components:
- **`frontend/`**: A pure HTML/CSS/JS application that provides a modern, guided user experience. It features premium animations, scroll-based journeys, and seamless inline results without page reloads.
- **`backend/`**: A lightning-fast FastAPI Python server that serves our Machine Learning models. It handles everything from NLP-based skill vectorization to complex scoring metrics.

## Project Structure

```text
CARYNTH/
├── frontend/                 # UI/UX Interface
│   ├── index.html            # Main SPA Layout
│   ├── style.css             # Premium Styling & Animations
│   └── script.js             # API Integration & Interaction Logic
├── backend/                  # AI & API Engine
│   ├── main.py               # FastAPI Server & Endpoints
│   ├── train_models.py       # ML Training Pipeline
│   ├── student_career_data.csv # Dataset
│   └── *.pkl                 # Pickled ML Models (RF, KMeans, NLP Encoders)
└── docs/                     # Technical Documentation
```

## Getting Started

### Prerequisites
- Python 3.8+
- A modern web browser

### 1. Running the Backend
1. Open a terminal and navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Install the required dependencies:
   ```bash
   pip install fastapi uvicorn pydantic scikit-learn numpy pandas
   ```
3. Start the FastAPI server using Uvicorn:
   ```bash
   uvicorn main:app --reload
   ```
   *The AI engine will now be listening at `http://127.0.0.1:8000`.*

### 2. Running the Frontend
1. Navigate to the frontend folder.
2. Double click the `index.html` file to open it in your browser. 
3. *Tip: For the best development experience, use VS Code with the "Live Server" extension to serve the `frontend/` directory.*

## Documentation
Additional technical details, NLP vectorization guides, and model architecture explanations can be found in the `docs/` folder.
