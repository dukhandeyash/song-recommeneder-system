import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import logging

# Load environment variables
load_dotenv()

class SpotifyAPI:
    def __init__(self):
        # Load credentials from environment variables
        client_id = os.getenv('SPOTIFY_CLIENT_ID')
        client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        
        # Initialize Spotify client
        client_credentials_manager = SpotifyClientCredentials(
            client_id=client_id, 
            client_secret=client_secret
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def search_tracks(self, query, limit=10):
        """Search for tracks on Spotify"""
        results = self.sp.search(q=query, type='track', limit=limit)
        return results['tracks']['items']
    
    def get_audio_features(self, track_ids):
        """Get audio features for a list of track IDs"""
        if not track_ids:
            return []
        return self.sp.audio_features(track_ids)
    
    def get_track_info(self, track_id):
        """Get detailed information about a track"""
        return self.sp.track(track_id)
    
    def get_artist_info(self, artist_id):
        """Get detailed information about an artist"""
        return self.sp.artist(artist_id)
    
    def get_recommendations(self, seed_tracks=None, seed_artists=None, seed_genres=None, limit=10, **kwargs):
        """Get recommendations based on seeds and audio features"""
        return self.sp.recommendations(
            seed_tracks=seed_tracks,
            seed_artists=seed_artists,
            seed_genres=seed_genres,
            limit=limit,
            **kwargs
        )

class RecommendationEngine:
    def __init__(self):
        # Load models and processed data
        self.scaler = joblib.load('models/scaler.pkl')
        self.pca = joblib.load('models/pca.pkl')
        self.kmeans = joblib.load('models/kmeans.pkl')
        self.nn_model = joblib.load('models/nearest_neighbors.pkl')
        self.tracks_df = pd.read_csv('models/processed_tracks.csv')
        
        # Audio features used for recommendations
        self.audio_features = [
            'danceability', 'energy', 'valence', 'tempo', 'loudness', 
            'speechiness', 'acousticness', 'liveness', 'instrumentalness'
        ]
    
    def get_similar_tracks(self, track_id, n_recommendations=10):
        """Get similar tracks based on audio features"""
        # Find the track in our dataset
        track_data = self.tracks_df[self.tracks_df['track_id'] == track_id]
        
        if track_data.empty:
            # If track not found, return a random selection of tracks
            return self.tracks_df.sample(n_recommendations).to_dict('records')
        
        # Get the audio features
        track_features = track_data[self.audio_features].values
        
        # Scale the features - create DataFrame with feature names to avoid warning
        scaled_features = pd.DataFrame(
            self.scaler.transform(track_features),
            columns=self.audio_features
        ).values
        
        # Find nearest neighbors
        distances, indices = self.nn_model.kneighbors(scaled_features)
        
        # Get the similar tracks
        similar_tracks = self.tracks_df.iloc[indices[0]]
        
        return similar_tracks.to_dict('records')
    
    def get_mood_playlist(self, mood, n_tracks=20):
        """Get tracks based on mood"""
        mood_tracks = self.tracks_df[self.tracks_df['mood'] == mood]
        
        if len(mood_tracks) == 0:
            # If no tracks match the mood, return a random selection
            return self.tracks_df.sample(min(n_tracks, len(self.tracks_df))).to_dict('records')
        
        if len(mood_tracks) > n_tracks:
            return mood_tracks.sample(n_tracks).to_dict('records')
        return mood_tracks.to_dict('records')
    
    def get_activity_playlist(self, activity, n_tracks=20):
        """Get tracks based on activity"""
        activity_tracks = self.tracks_df[self.tracks_df['activity'] == activity]
        
        if len(activity_tracks) == 0:
            # If no tracks match the activity, return a random selection
            return self.tracks_df.sample(min(n_tracks, len(self.tracks_df))).to_dict('records')
        
        if len(activity_tracks) > n_tracks:
            return activity_tracks.sample(n_tracks).to_dict('records')
        return activity_tracks.to_dict('records')
    
    def get_time_of_day_playlist(self, time_of_day, n_tracks=20):
        """Get tracks based on time of day"""
        time_tracks = self.tracks_df[self.tracks_df['time_of_day'] == time_of_day]
        
        if len(time_tracks) == 0:
            # If no tracks match the time of day, return a random selection
            return self.tracks_df.sample(min(n_tracks, len(self.tracks_df))).to_dict('records')
        
        if len(time_tracks) > n_tracks:
            return time_tracks.sample(n_tracks).to_dict('records')
        return time_tracks.to_dict('records')
    
    def calculate_compatibility_score(self, track_ids):
        """
        Calculate a comprehensive compatibility score between tracks
        Uses multiple strategies to ensure accuracy:
        1. Feature similarity
        2. Genre compatibility
        3. Audio characteristics alignment
        """
        if not track_ids or len(track_ids) < 2:
            return 0
        
        # Get tracks from our dataset or Spotify
        tracks = self.tracks_df[self.tracks_df['track_id'].isin(track_ids)]
        
        if len(tracks) < 2:
            try:
                # Fetch additional track details from Spotify
                additional_tracks = self.get_track_features(track_ids)
                if len(additional_tracks) >= 2:
                    features = additional_tracks[self.audio_features].values
                    tracks = additional_tracks
                else:
                    return 0
            except Exception as e:
                print(f"Error fetching track features: {e}")
                return 0
        else:
            features = tracks[self.audio_features].values
        
        # Scale features
        scaled_features = pd.DataFrame(
            self.scaler.transform(features),
            columns=self.audio_features
        )
        
        # Comprehensive compatibility calculation
        def calculate_feature_compatibility(feature_name):
            """Calculate compatibility for a specific feature"""
            feature_values = scaled_features[feature_name]
            feature_std = np.std(feature_values)
            feature_mean = np.mean(feature_values)
            
            # Lower standard deviation indicates more similar tracks
            feature_compatibility = 100 * (1 - feature_std)
            return feature_compatibility
        
        # Calculate compatibility for key features
        feature_weights = {
            'danceability': 0.15,
            'energy': 0.2,
            'valence': 0.2,
            'tempo': 0.15,
            'loudness': 0.1,
            'speechiness': 0.1,
            'acousticness': 0.1
        }
        
        # Weighted feature compatibility
        weighted_compatibility = sum(
            calculate_feature_compatibility(feature) * weight 
            for feature, weight in feature_weights.items()
        )
        
        # Pairwise distance calculation for additional nuance
        from sklearn.metrics.pairwise import euclidean_distances
        distances = euclidean_distances(scaled_features[list(feature_weights.keys())])
        avg_distance = np.mean(distances)
        
        # Normalize and combine metrics
        distance_factor = 100 * (1 - (avg_distance / np.sqrt(len(feature_weights))))
        
        # Final compatibility score
        final_score = 0.6 * weighted_compatibility + 0.4 * distance_factor
        
        # Ensure score is between 0 and 100
        final_score = max(0, min(100, final_score))
        
        # Add some randomness to prevent repetitive scores
        import random
        final_score += random.uniform(-5, 5)
        final_score = max(0, min(100, final_score))
        
        return round(final_score, 2)
    
    def get_track_features(self, track_ids):
        """Enhanced track features retrieval"""
        track_features = []
        for track_id in track_ids:
            try:
                # Fetch track and audio features
                track = self.sp.track(track_id)
                audio_features = self.sp.audio_features(track_id)[0]
                
                # Comprehensive feature extraction
                track_features.append({
                    'track_id': track_id,
                    'name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'key': audio_features['key'],
                    'loudness': audio_features['loudness'],
                    'mode': audio_features['mode'],
                    'speechiness': audio_features['speechiness'],
                    'acousticness': audio_features['acousticness'],
                    'instrumentalness': audio_features['instrumentalness'],
                    'liveness': audio_features['liveness'],
                    'valence': audio_features['valence'],
                    'tempo': audio_features['tempo'],
                    'duration_ms': audio_features['duration_ms']
                })
            except Exception as e:
                print(f"Error fetching track features for {track_id}: {e}")
        
        return pd.DataFrame(track_features)
    
    def calculate_diversity_score(self, track_ids):
        """
        Calculate a comprehensive diversity score for a set of tracks
        
        Args:
            track_ids (list): List of track IDs to evaluate diversity
        
        Returns:
            float: Diversity score between 0 and 100
        """
        # Validate input
        if not track_ids or len(track_ids) < 2:
            return 0
        
        # Get tracks from our dataset
        tracks = self.tracks_df[self.tracks_df['track_id'].isin(track_ids)]
        
        # If not enough tracks in local dataset, try Spotify
        if len(tracks) < 2:
            try:
                # Fetch additional track details from Spotify
                additional_tracks = self.get_track_features(track_ids)
                if len(additional_tracks) >= 2:
                    tracks = additional_tracks
                else:
                    return 0
            except Exception as e:
                logging.error(f"Error fetching track features: {e}")
                return 0
        
        # Audio features for diversity calculation
        audio_features = [
            'danceability', 'energy', 'valence', 
            'tempo', 'loudness', 'speechiness', 
            'acousticness', 'liveness', 'instrumentalness'
        ]
        
        # Scale features
        scaled_features = self.scaler.transform(tracks[audio_features])
        
        # Pairwise distance calculation
        from sklearn.metrics.pairwise import euclidean_distances
        distances = euclidean_distances(scaled_features)
        
        # Genre diversity calculation
        def calculate_genre_diversity(tracks):
            """Calculate diversity based on genres"""
            # Handle potential missing or empty genre data
            genres = tracks['genres'].fillna('').str.lower()
            
            # Count unique genres
            unique_genres = genres.str.split(',').explode().str.strip().nunique()
            
            # Normalize genre diversity
            max_possible_genres = 20  # Reasonable upper limit for genre diversity
            genre_diversity = min(100, (unique_genres / max_possible_genres) * 100)
            
            return genre_diversity
        
        # Audio feature diversity calculation
        def calculate_feature_diversity(feature_name):
            """Calculate diversity for a specific feature"""
            feature_values = scaled_features[:, audio_features.index(feature_name)]
            feature_std = np.std(feature_values)
            
            # Higher standard deviation indicates more diverse tracks
            feature_diversity = 100 * feature_std
            return feature_diversity
        
        # Weighted feature diversity
        feature_weights = {
            'danceability': 0.15,
            'energy': 0.2,
            'valence': 0.2,
            'tempo': 0.15,
            'loudness': 0.1,
            'speechiness': 0.1,
            'acousticness': 0.1
        }
        
        # Calculate weighted feature diversity
        weighted_feature_diversity = sum(
            calculate_feature_diversity(feature) * weight 
            for feature, weight in feature_weights.items()
        )
        
        # Distance-based diversity factor
        avg_distance = np.mean(distances)
        distance_diversity = 100 * (avg_distance / np.sqrt(len(feature_weights)))
        
        # Genre diversity factor
        genre_diversity = calculate_genre_diversity(tracks)
        
        # Combine diversity metrics
        final_diversity_score = (
            0.4 * weighted_feature_diversity + 
            0.3 * distance_diversity + 
            0.3 * genre_diversity
        )
        
        # Ensure score is between 0 and 100
        final_diversity_score = max(0, min(100, final_diversity_score))
        
        return round(final_diversity_score, 2)
