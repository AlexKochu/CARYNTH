from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pickle
import numpy as np
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Initialize App
app = FastAPI(title="Career Architect API", description="Student Career Recommendation System")

# CORS (Allow frontend to connect)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development; restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Load Models
print("Loading models...")
def load_pkl(filename):
    with open(filename, 'rb') as f:
        return pickle.load(f)

# Global variables to store models
models = {}

# Define tokenizer for unpickling validation
def skill_tokenizer(text):
    return [x.strip() for x in text.split(',')]

import sys

# Inject into __main__ to fix pickle loading issue if it expects it there
if not hasattr(sys.modules['__main__'], 'skill_tokenizer'):
    setattr(sys.modules['__main__'], 'skill_tokenizer', skill_tokenizer)

@app.on_event("startup")
def load_models():
    print("Loading models...")
    try:
        models['rf_model'] = load_pkl('career_rf_model.pkl')
        models['cluster_model'] = load_pkl('career_cluster_model.pkl')
        models['skill_vectorizer'] = load_pkl('skill_vectorizer.pkl')
        models['interest_encoder'] = load_pkl('interest_encoder.pkl')
        models['role_encoder'] = load_pkl('role_encoder.pkl')
        print("Models loaded successfully.")
    except Exception as e:
        print(f"CRITICAL ERROR loading models: {e}")

# 3. Request/Response Models
class StudentProfile(BaseModel):
    cgpa: float
    interest: str
    skills: str  # Comma separated
    courses_completed: int
    projects_count: int

class PredictionResponse(BaseModel):
    predicted_role: str
    cluster_id: int
    skill_gap: list[str]
    learning_path: list[str]
    career_score: float

# 4. Helper Functions / NLP Layer

# CANONICAL ONTOLOGY
# Maps canonical skill keys to list of synonyms/variations
CANONICAL_SKILL_MAP = {
    "neuralnetworks": ["neural networks", "neural_networks", "nn", "deep learning", "deeplearning"],
    "pytorch": ["pytorch", "torch"],
    "scikitlearn": ["scikit-learn", "sklearn", "scikit learn", "scikit"],
    "numpy": ["numpy", "np"],
    "pandas": ["pandas", "pd"],
    "statistics": ["stats", "statistics", "statistical analysis", "math", "mathematics"],
    "sql": ["sql", "mysql", "postgresql", "postgres", "nosql", "database", "databases"],
    "python": ["python", "py"],
    "machinelearning": ["machine learning", "ml", "machinelearning"],
    "datavisualization": ["data visualization", "visualization", "tableau", "power bi", "matplotlib", "seaborn"],
    "javascript": ["javascript", "js", "es6"],
    "react": ["react", "react.js", "reactjs"],
    "node": ["node.js", "node", "nodejs", "express"],
    "java": ["java", "j2ee"],
    "c++": ["c++", "cpp"],
    "datastructures": ["data structures", "dsa", "algorithms", "system design"],
    "cloud": ["cloud computing", "aws", "azure", "gcp", "docker", "kubernetes", "devops"],
    "cybersecurity": ["cyber security", "security", "network security", "hacking", "cryptography"],
    "excel": ["excel", "microsoft excel", "spreadsheets"],
    "git": ["git", "github", "version control"]
}

# Invert map for O(1) lookup: "nn" -> "neuralnetworks"
SKILL_LOOKUP = {}
for canonical, variants in CANONICAL_SKILL_MAP.items():
    SKILL_LOOKUP[canonical] = canonical # Map self to self
    for v in variants:
        SKILL_LOOKUP[v] = canonical

def normalize_skill(skill_text):
    """
    NLP Preprocessing:
    1. Lowercase
    2. Remove special chars (hyphens, dots become spaces or removed)
    3. Remove underscores
    4. Map to canonical form via dictionary
    """
    if not skill_text: 
        return ""
    
    # 1. Lowercase and basic cleanup
    clean = skill_text.lower().strip()
    
    # 2. Check lookup directly first (handles "node.js" -> "node")
    if clean in SKILL_LOOKUP:
        return SKILL_LOOKUP[clean]
    
    # 3. Aggressive normalization if direct match fails
    # Remove all non-alphanumeric except maybe + # (for C++, C#)
    # Ideally "c++" -> "c++" (in dict). "neural-networks" -> "neuralnetworks"
    # Simple strategy: remove spaces, hyphens, underscores to create "neuralnetworks"
    import re
    # Remove spaces, -, _, .
    compressed = re.sub(r'[\s\-_.]', '', clean)
    
    if compressed in SKILL_LOOKUP:
        return SKILL_LOOKUP[compressed]
    
    # Return compressed or original if no map found (fallback)
    return compressed if compressed else clean

def calculate_skill_gap(user_skills_list, predicted_role):
    # Expanded database of required skills per role with weights (for reference, but using weighted map below for consistency)
    # This gap function returns MISSING skills.
    
    # Required skills map (using human readable/canonical intent)
    role_skills_map = {
        "AI/ML Engineer": ["python", "tensorflow", "pytorch", "scikitlearn", "deeplearning", "neuralnetworks", "mathematics"],
        "Data Scientist": ["python", "statistics", "machinelearning", "pandas", "numpy", "sql", "datavisualization"],
        "Web Developer": ["html", "css", "javascript", "react", "node", "sql", "api"],
        "Software Engineer": ["java", "c++", "datastructures", "algorithms", "system design", "sql", "git"],
        "Data Analyst": ["excel", "sql", "datavisualization", "python", "statistics"],
        "App Development": ["flutter", "react native", "swift", "kotlin", "java", "firebase"],
        "Cyber Security": ["cybersecurity", "cryptography", "linux", "python"],
        "Cloud Computing": ["cloud", "linux", "networking"]
    }
    
    # Normalize user skills to set of canonicals
    user_canonicals = set()
    for s in user_skills_list:
        norm = normalize_skill(s)
        if norm: user_canonicals.add(norm)
    
    # Get required skills
    required_skills = role_skills_map.get(predicted_role, ["communication", "problem solving"])
    
    # Normalize required skills (just in case map has non-canonicals)
    req_canonicals = [normalize_skill(s) for s in required_skills]
    
    # Find missing
    missing_intents = [s for s in req_canonicals if s not in user_canonicals]
    
    # Convert canonical IDs back to readable labels for UI
    # Map "neuralnetworks" -> "Neural Networks"
    # Simple heuristic: title case the canonical or use a display map.
    # For now, we title case, but special handling for acronyms like 'sql'.
    display_map = {
        "neuralnetworks": "Neural Networks",
        "deeplearning": "Deep Learning",
        "machinelearning": "Machine Learning",
        "scikitlearn": "Scikit-Learn",
        "datavisualization": "Data Visualization",
        "datastructures": "Data Structures & Algo",
        "cybersecurity": "Cyber Security",
        "artificialintelligence": "AI",
        "nlp": "NLP",
        "api": "API",
        "dsa": "Data Structures",
        "uiux": "UI/UX"
    }
    
    readable_missing = []
    for m in missing_intents:
        if m in display_map:
            readable_missing.append(display_map[m])
        else:
            readable_missing.append(m.upper() if len(m) <= 3 else m.title())
            
    return readable_missing

def generate_learning_path(skill_gaps, role):
    path = []
    if not skill_gaps:
        path.append(f"Advanced {role} Certification")
        path.append("Open Source Contributions")
        path.append("Leadership & Soft Skills")
    else:
        # Simple logic: suggest courses for first 3 gaps
        for gap in skill_gaps[:3]:
            path.append(f"Learn {gap} Fundamentals")
        if len(skill_gaps) > 3:
            path.append(f"Master remaining skills for {role}")
        
    return path

def calculate_readiness_score(user_skills_list, predicted_role, cgpa, projects):
    """
    Scientific Scoring Model:
    - Core Skills Weight: 80% (Sum of matched skill weights)
    - CGPA Weight: 10%
    - Projects Weight: 10%
    """
    
    # 1. Define Weighted Maps for Roles (Using Canonical Keys)
    # Weights sum to 1.0 (100%) for the Skill Portion.
    weighted_skill_map = {
        "Data Scientist": {
            "python": 0.25,
            "statistics": 0.20,
            "machinelearning": 0.20,
            "pandas": 0.15,
            "numpy": 0.15,
            "sql": 0.10,
            "datavisualization": 0.10
        },
        "AI/ML Engineer": {
            "python": 0.20,
            "tensorflow": 0.20,
            "pytorch": 0.20,
            "scikitlearn": 0.15,
            "deeplearning": 0.15,
            "mathematics": 0.10
        },
        "Software Engineer": {
            "java": 0.20,
            "c++": 0.20,
            "datastructures": 0.50, # Combined DSA + Sys Design
            "git": 0.10
        },
        "Web Developer": {
            "javascript": 0.30,
            "react": 0.20,
            "html": 0.15,
            "css": 0.15,
            "node": 0.20
        },
        "Data Analyst": {
            "sql": 0.30,
            "excel": 0.20,
            "datavisualization": 0.20,
            "python": 0.15,
            "statistics": 0.15
        }
    }
    
    # Check if role exists in map
    role_weights = weighted_skill_map.get(predicted_role)
    
    # Normalize user skills
    user_canonicals = set()
    for s in user_skills_list:
        norm = normalize_skill(s)
        if norm: user_canonicals.add(norm)
    
    # 2. Calculate Skill Match Score (Max 80 points)
    skill_score_raw = 0.0
    
    if role_weights:
        # Weighted model
        matched_weights = 0.0
        for skill_key, weight in role_weights.items():
            # Check if canonical skill_key is in user skills
            # Also handle if user has "pytorch" but key is "tensorflow" (no match)
            # Logic: Exact match on canonical tokens
            if skill_key in user_canonicals:
                matched_weights += weight
        
        # Cap at 1.0
        skill_score_raw = min(1.0, matched_weights)
        
    else:
        # Fallback
        required_skills = ["python", "problemsolving", "communication"]
        match_count = sum(1 for s in required_skills if s in user_canonicals)
        skill_score_raw = match_count / len(required_skills)

    # Weighted Contribution: Skills = 80%
    weighted_skill_score = skill_score_raw * 80
    
    # 3. CGPA Contribution (Max 10 points)
    cgpa_score = min(10.0, cgpa) if cgpa else 0.0
    
    # 4. Projects Contribution (Max 10 points)
    project_score = min(10.0, projects * 2.0)
    
    # 5. Total Score
    total_score = weighted_skill_score + cgpa_score + project_score
    
    # WARNING: Penalize if NO core skills found
    if skill_score_raw < 0.1: 
        total_score = min(total_score, 15.0)
        
    return total_score

# 5. Prediction Endpoint
@app.post("/predict", response_model=PredictionResponse)
def predict_career(profile: StudentProfile):
    try:
        # a. Preprocess Inputs
        # Encode Interest
        try:
            # Handle unseen labels by assigning a default or closest (here just using fit equivalent if possible, but safely we should use what we have)
            # transform expects an array
            # If interest is not in encoder classes, it will error. 
            # Ideally we check classes. For MVP, we might wrap in try/except or use a fallback.
            if profile.interest not in models['interest_encoder'].classes_:
                 # Fallback: Use the mode or 0
                 interest_encoded = 0 
            else:
                 interest_encoded = models['interest_encoder'].transform([profile.interest])[0]
        except:
            interest_encoded = 0

        # Vectorize Skills
        user_skills_list = [s.strip() for s in profile.skills.split(',')]
        # vectorizer transform expects iterable of strings (documents)
        skill_matrix = models['skill_vectorizer'].transform([profile.skills])
        
        # Prepare Feature Vector
        # Structure must match training: CGPA, Interest_Encoded, Courses, Projects, Skills...
        X_skills = skill_matrix.toarray()
        X_other = np.array([[
            profile.cgpa, 
            interest_encoded, 
            profile.courses_completed, 
            profile.projects_count
        ]])
        
        X_input = np.hstack((X_other, X_skills))
        
        # b. Predict Role
        role_label = models['rf_model'].predict(X_input)[0]
        predicted_role = models['role_encoder'].inverse_transform([role_label])[0]
        
        # c. Predict Cluster
        cluster_id = models['cluster_model'].predict(X_input)[0]
        
        # d. Post-processing (Gaps, Path, Score)
        skill_gaps = calculate_skill_gap(user_skills_list, predicted_role)
        learning_path = generate_learning_path(skill_gaps, predicted_role)
        
        # Calculate Score
        career_score = calculate_readiness_score(user_skills_list, predicted_role, profile.cgpa, profile.projects_count)
        
        # Handle Low Readiness Warning via Skill Gap Injection (Optional but helpful)
        if career_score < 20 and not any("Low readiness" in g for g in skill_gaps):
            skill_gaps.insert(0, "CRITICAL: Low readiness - Foundational skills missing")
        
        return {
            "predicted_role": predicted_role,
            "cluster_id": int(cluster_id),
            "skill_gap": skill_gaps,
            "learning_path": learning_path,
            "career_score": float(career_score)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Career Architect API is running"}
