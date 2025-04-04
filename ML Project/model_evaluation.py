import pandas as pd
import numpy as np
import joblib
import os
import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score, 
    precision_score, 
    recall_score, 
    f1_score, 
    confusion_matrix, 
    classification_report
)
from sklearn.preprocessing import LabelEncoder

def load_models_and_data():
    """Load pre-trained models and processed data."""
    print("Loading models and data...")
    
    # Check if model files exist
    model_files = [
        'models/processed_tracks.csv',
        'models/scaler.pkl',
        'models/pca.pkl',
        'models/kmeans.pkl',
        'models/nearest_neighbors.pkl'
    ]
    
    for file in model_files:
        if not os.path.exists(file):
            print(f"Error: File {file} not found. Please run train_model.py first.")
            sys.exit(1)
    
    # Load processed tracks
    try:
        features_df = pd.read_csv('models/processed_tracks.csv')
    except Exception as e:
        print(f"Error loading processed tracks: {e}")
        sys.exit(1)
    
    # Load trained models
    try:
        scaler = joblib.load('models/scaler.pkl')
        pca = joblib.load('models/pca.pkl')
        kmeans = joblib.load('models/kmeans.pkl')
        nn_model = joblib.load('models/nearest_neighbors.pkl')
    except Exception as e:
        print(f"Error loading trained models: {e}")
        sys.exit(1)
    
    return features_df, scaler, pca, kmeans, nn_model

def evaluate_clustering_performance(features_df, kmeans):
    """
    Evaluate clustering performance using multiple metrics.
    """
    from sklearn.metrics import (
        silhouette_score, 
        calinski_harabasz_score, 
        davies_bouldin_score
    )
    
    # Select audio features for clustering
    audio_features = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 
                      'speechiness', 'acousticness', 'liveness', 'instrumentalness']
    
    # Prepare data
    X = features_df[audio_features]
    
    # Clustering metrics
    print("\n--- Clustering Performance Metrics ---")
    try:
        print(f"Silhouette Score: {silhouette_score(X, kmeans.labels_):.4f}")
        print(f"Calinski-Harabasz Index: {calinski_harabasz_score(X, kmeans.labels_):.4f}")
        print(f"Davies-Bouldin Index: {davies_bouldin_score(X, kmeans.labels_):.4f}")
    except Exception as e:
        print(f"Error calculating clustering metrics: {e}")

def evaluate_mood_classification(features_df):
    """
    Evaluate mood classification performance.
    """
    # Prepare data for mood classification
    X = features_df[['danceability', 'energy', 'valence', 'tempo', 'loudness', 
                     'speechiness', 'acousticness', 'liveness', 'instrumentalness']]
    y = features_df['mood']
    
    # Encode mood labels
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
    
    # Train a simple classifier (Random Forest)
    from sklearn.ensemble import RandomForestClassifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    try:
        clf.fit(X_train, y_train)
    except Exception as e:
        print(f"Error training classifier: {e}")
        return
    
    # Predictions
    try:
        y_pred = clf.predict(X_test)
    except Exception as e:
        print(f"Error making predictions: {e}")
        return
    
    # Print detailed classification report
    print("\n--- Mood Classification Performance ---")
    print("Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    
    # Detailed metrics
    print("\n--- Detailed Metrics ---")
    try:
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print(f"Precision (Macro): {precision_score(y_test, y_pred, average='macro'):.4f}")
        print(f"Recall (Macro): {recall_score(y_test, y_pred, average='macro'):.4f}")
        print(f"F1 Score (Macro): {f1_score(y_test, y_pred, average='macro'):.4f}")
    except Exception as e:
        print(f"Error calculating classification metrics: {e}")

def main():
    # Load models and data
    try:
        features_df, scaler, pca, kmeans, nn_model = load_models_and_data()
    except Exception as e:
        print(f"Error loading models and data: {e}")
        return
    
    # Evaluate clustering performance
    evaluate_clustering_performance(features_df, kmeans)
    
    # Evaluate mood classification
    evaluate_mood_classification(features_df)

if __name__ == "__main__":
    main()
