# Master Class: NLP & Vectorization in Your Project

This guide answers **"Where is the code?"** and **"What does it actually do?"** for the advanced AI parts of your system.

---

## Part 1: NLP Code (Skill Normalization)
**Location**: `main.py` (Lines ~65 to ~130)

### 1. Where involves the "Brain" (The Ontology)?
Look at the big dictionary called `CANONICAL_SKILL_MAP` in `main.py`.
```python
# main.py

CANONICAL_SKILL_MAP = {
    "neuralnetworks": ["nn", "deep learning", "neural networks"],
    "pytorch": ["torch", "pytorch"],
    ...
}
```
**What it does**: This is your AI's "vocabulary". It knows that "nn" and "deep learning" are just nicknames for `neuralnetworks`.

### 2. Where involves the "Logic" (The Function)?
Look at the function `normalize_skill(skill_text)` in `main.py`.
```python
# main.py

def normalize_skill(skill_text):
    clean = skill_text.lower().strip()  # Step A: Lowercase
    # ...
    if compressed in SKILL_LOOKUP:      # Step B: Check Dictionary
        return SKILL_LOOKUP[compressed]
```
**What it does**:
1.  **Step A**: Takes messy input ("  ReaCT.js  ").
2.  **Step B**: Cleans it ("reactjs").
3.  **Step C**: Finds the official name in the dictionary.
4.  **Result**: Returns the clean, standard ID that the model understands.

---

## Part 2: Vectorization (Turning Text to Numbers)
**Location**: `train_models.py` (Lines ~22-27) AND `main.py` (Line ~130)

### What is Vectorization?
Computers **cannot** understand text like "Python". They only understand numbers.
Vectorization turns a list of skills into a row of 0s and 1s.

**Example**:
Imagine all possible skills are: `[Python, Java, SQL]`.
*   User A has "Python, SQL" -> Vector: `[1, 0, 1]` (Yes Python, No Java, Yes SQL).
*   User B has "Java" -> Vector: `[0, 1, 0]`.

### 1. Where do we TEACH the vectorizer (Training)?
In `train_models.py`:
```python
# train_models.py

# 1. Create the Tool
skill_vectorizer = CountVectorizer(tokenizer=skill_tokenizer)

# 2. Teach it ALL the skills from your CSV
skill_matrix = skill_vectorizer.fit_transform(df['Skills'])
```
*   `fit`: Learn the vocabulary (e.g., "Ah, 'Python' is column 0, 'Java' is column 1").
*   `transform`: Convert the CSV text into the number matrix.

### 2. Where do we USE it (Inference)?
In `main.py`:
```python
# main.py inside predict_career()

# Take the user's ONE string
skill_matrix = models['skill_vectorizer'].transform([profile.skills])
```
*   **Crucial Note**: We call `transform`, NOT `fit`. We must use the *exact same* dictionary we learned during training.

---

## Part 3: The "Extra Python Code" (FastAPI)
**Location**: `main.py` (Top and Bottom)

### The API Layer
```python
app = FastAPI(...)

@app.post("/predict")
def predict_career(profile: StudentProfile):
    # ...
```
**What it does**:
*   Normally, Python functions sit on your laptop waiting.
*   **FastAPI** wraps that function in a **Web Server**.
*   It listens for internet traffic (HTTP Requests) on port 8000.
*   When `index.html` sends data, FastAPI catches it, passes it to your `normalize_skill` -> `vectorizer` -> `model`, and sends the answer back.

---

## Summary for Viva/Interview

1.  **"How do you handle synonyms?"**
    *   "I implemented a custom **NLP Normalization Layer** in `main.py` using a canonical ontology map."

2.  **"How does the model understand text?"**
    *   "I used **CountVectorizer** (Bag of Words) to convert text skills into sparse numerical vectors."

3.  **"How is it deployed?"**
    *   "I built a **FastAPI** backend to serve the model as a REST endpoint, allowing real-time inference from the dashboard."
