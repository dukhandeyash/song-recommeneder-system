import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import NearestNeighbors
import joblib
import os

print("Loading dataset...")
# Load the dataset
df = pd.read_csv("spotify_data_with_instrumentalness.csv")

# Remove duplicates
df_nodup = df.drop_duplicates(subset=['track_id'])

# Fill missing values
df_nodup['genres'] = df_nodup['genres'].fillna('')

# Select features for clustering and recommendation
audio_features = ['danceability', 'energy', 'valence', 'tempo', 'loudness', 
                 'speechiness', 'acousticness', 'liveness', 'instrumentalness']

# Create a copy of the dataset with only the needed columns
features_df = df_nodup[['track_id', 'track_name', 'artist', 'album', 'release_year', 'genres'] + audio_features].copy()

# Normalize the audio features
scaler = StandardScaler()
features_scaled = pd.DataFrame(scaler.fit_transform(features_df[audio_features]), columns=audio_features)

print("Training models...")
# Dimensionality reduction with PCA
pca = PCA(n_components=3)
features_pca = pca.fit_transform(features_scaled.values)

# Clustering for mood/genre categorization
kmeans = KMeans(n_clusters=8, random_state=42)
clusters = kmeans.fit_predict(features_scaled.values)
features_df['cluster'] = clusters

# Create a nearest neighbors model for recommendations
nn_model = NearestNeighbors(n_neighbors=10, algorithm='auto')
nn_model.fit(features_scaled.values)

# Create mood mappings based on audio features
def assign_mood(row):
    # High valence and energy = Happy
    if row['valence'] > 0.6 and row['energy'] > 0.6:
        return 'Happy'
    # Low valence, high energy = Angry
    elif row['valence'] < 0.4 and row['energy'] > 0.6:
        return 'Angry'
    # High valence, low energy = Relaxed
    elif row['valence'] > 0.6 and row['energy'] < 0.4:
        return 'Relaxed'
    # Low valence, low energy = Sad
    elif row['valence'] < 0.4 and row['energy'] < 0.4:
        return 'Sad'
    # Everything else = Neutral
    else:
        return 'Neutral'

# Assign moods to each track
features_df['mood'] = features_df.apply(assign_mood, axis=1)

# Create activity mappings
def assign_activity(row):
    # High tempo and energy = Workout
    if row['tempo'] > 120 and row['energy'] > 0.7:
        return 'Workout'
    # High acousticness, low energy = Study/Focus
    elif row['acousticness'] > 0.6 and row['energy'] < 0.5:
        return 'Study/Focus'
    # High danceability and energy = Party
    elif row['danceability'] > 0.7 and row['energy'] > 0.6:
        return 'Party'
    # Moderate tempo, low energy = Relaxation
    elif 70 <= row['tempo'] <= 110 and row['energy'] < 0.4:
        return 'Relaxation'
    # Everything else = General
    else:
        return 'General'

# Assign activities to each track
features_df['activity'] = features_df.apply(assign_activity, axis=1)

# Create time-of-day mappings
def assign_time_of_day(row):
    # High energy and tempo = Morning
    if row['energy'] > 0.7 and row['tempo'] > 110:
        return 'Morning'
    # Moderate energy and valence = Afternoon
    elif 0.4 <= row['energy'] <= 0.7 and row['valence'] >= 0.5:
        return 'Afternoon'
    # Low energy, low tempo = Evening
    elif row['energy'] < 0.4 and row['tempo'] < 100:
        return 'Evening'
    # Low energy, high valence = Night
    elif row['energy'] < 0.5 and row['valence'] > 0.6:
        return 'Night'
    # Everything else = Any Time
    else:
        return 'Any Time'

# Assign time of day to each track
features_df['time_of_day'] = features_df.apply(assign_time_of_day, axis=1)

# Save the models and processed data
print("Saving models and processed data...")
os.makedirs('models', exist_ok=True)
joblib.dump(scaler, 'models/scaler.pkl')
joblib.dump(pca, 'models/pca.pkl')
joblib.dump(kmeans, 'models/kmeans.pkl')
joblib.dump(nn_model, 'models/nearest_neighbors.pkl')

# Save the processed dataframe
features_df.to_csv('models/processed_tracks.csv', index=False)

print("Model training complete!")
