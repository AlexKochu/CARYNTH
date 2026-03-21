import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans

# 1. Load Data
print("Loading data...")
df = pd.read_csv("student_career_data.csv")
print(f"Data loaded: {df.shape}")

# 2. Preprocessing
# Encoding Interests
print("Encoding interests...")
interest_encoder = LabelEncoder()
df['Interest_Encoded'] = interest_encoder.fit_transform(df['Interests'])

# Vectorizing Skills
print("Vectorizing skills...")
def skill_tokenizer(text):
    return [x.strip() for x in text.split(',')]

skill_vectorizer = CountVectorizer(tokenizer=skill_tokenizer)
skill_matrix = skill_vectorizer.fit_transform(df['Skills'])

# Prepare Features
# Features: CGPA, Interest_Encoded, Skills (vectorized - expanding to dense)
# We need to combine scalar features with the sparse matrix from CountVectorizer
X_skills = skill_matrix.toarray()
X_other = df[['CGPA', 'Interest_Encoded', 'Courses_Completed', 'Projects_Count']].values
X = np.hstack((X_other, X_skills))

# Target for Role Prediction
role_encoder = LabelEncoder()
y_role = role_encoder.fit_transform(df['Role'])

# 3. Model Training
# Train Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y_role, test_size=0.2, random_state=42)

# Random Forest for Role Prediction
print("Training Random Forest for Job Role Prediction...")
rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
print(f"RF Training Accuracy: {rf_model.score(X_train, y_train):.4f}")
print(f"RF Test Accuracy: {rf_model.score(X_test, y_test):.4f}")

# KMeans for Student Clustering
# We use the same features X
print("Training KMeans for Student Clustering...")
kmeans_model = KMeans(n_clusters=5, random_state=42) # Assuming 5 clusters
clusters = kmeans_model.fit_predict(X)
df['Cluster'] = clusters

# 4. Save Models
print("Saving models...")
def save_pkl(obj, filename):
    with open(filename, 'wb') as f:
        pickle.dump(obj, f)
    print(f"Saved {filename}")

save_pkl(rf_model, 'career_rf_model.pkl')
save_pkl(kmeans_model, 'career_cluster_model.pkl')
save_pkl(skill_vectorizer, 'skill_vectorizer.pkl')
save_pkl(interest_encoder, 'interest_encoder.pkl')
save_pkl(role_encoder, 'role_encoder.pkl')

print("All models trained and saved successfully.")
