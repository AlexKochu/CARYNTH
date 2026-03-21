import pickle
import numpy as np
import pandas as pd
import sklearn

# Define dummy tokenizer to satisfy pickle
def skill_tokenizer(text):
    return text.split(',')

def load_pkl(path):
    print(f"Loading {path}...")
    try:
        with open(path, 'rb') as f:
            obj = pickle.load(f)
            return obj
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# Load models
rf_model = load_pkl('career_rf_model.pkl')
cluster_model = load_pkl('career_cluster_model.pkl')
skill_vectorizer = load_pkl('skill_vectorizer.pkl')
interest_encoder = load_pkl('interest_encoder.pkl')
role_encoder = load_pkl('role_encoder.pkl')

print("\n--- Detailed Inspection ---")

# Inspect RF Model
if rf_model is not None:
    print(f"RF Model Type: {type(rf_model)}")
    if isinstance(rf_model, np.ndarray):
        print(f"RF Model is an array with shape: {rf_model.shape}")
        # Check first element type
        if rf_model.size > 0:
            print(f"First element type: {type(rf_model.flat[0])}")
    elif hasattr(rf_model, 'n_features_in_'):
        print(f"RF n_features_in_: {rf_model.n_features_in_}")
        if hasattr(rf_model, 'feature_names_in_'):
            print(f"RF feature_names_in_: {rf_model.feature_names_in_}")
    else:
        print(f"RF Model has no n_features_in_. attributes: {dir(rf_model)[:10]}")

# Inspect Cluster Model
if cluster_model is not None:
    print(f"\nCluster Model Type: {type(cluster_model)}")
    if isinstance(cluster_model, np.ndarray):
        print(f"Cluster Model is an array with shape: {cluster_model.shape}")
    elif hasattr(cluster_model, 'n_features_in_'):
        print(f"Cluster n_features_in_: {cluster_model.n_features_in_}")

# Inspect Skill Vectorizer
if skill_vectorizer is not None:
    print(f"\nSkill Vectorizer Type: {type(skill_vectorizer)}")
    if hasattr(skill_vectorizer, 'get_feature_names_out'):
        try:
             feats = skill_vectorizer.get_feature_names_out()
             print(f"Skill Feature Names count: {len(feats)}")
             print(f"Sample features: {feats[:5]}")
        except:
             print("Could not get feature names")

# Inspect Encoders
if interest_encoder is not None:
    print(f"\nInterest Encoder Type: {type(interest_encoder)}")
    if hasattr(interest_encoder, 'classes_'):
        print(f"Interest Classes: {interest_encoder.classes_}")

if role_encoder is not None:
    print(f"\nRole Encoder Type: {type(role_encoder)}")
    if hasattr(role_encoder, 'classes_'):
        print(f"Role Classes: {role_encoder.classes_}")
