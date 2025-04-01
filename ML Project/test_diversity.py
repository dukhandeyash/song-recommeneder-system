import os
import sys
import pandas as pd
import numpy as np
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Dynamically add project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(project_dir)

# Import dependencies
import joblib
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import euclidean_distances

# Load necessary components
class RecommendationEngine:
    def __init__(self, dataset_path):
        # Load dataset
        logging.info("Loading dataset...")
        self.tracks_df = pd.read_csv(dataset_path)
        
        # Define audio features for diversity calculation
        self.audio_features = [
            'danceability', 'energy', 'valence', 
            'tempo', 'loudness', 'speechiness', 
            'acousticness', 'liveness', 'instrumentalness'
        ]
        
        # Define genre features
        self.genre_features = ['genres']
        
        # Create scaler if not exists
        logging.info("Preparing scaler...")
        scaler_path = os.path.join(project_dir, 'scaler.joblib')
        
        if not os.path.exists(scaler_path):
            # Create and fit scaler
            features_for_scaling = self.tracks_df[self.audio_features]
            self.scaler = StandardScaler()
            self.scaler.fit(features_for_scaling)
            
            # Save scaler
            joblib.dump(self.scaler, scaler_path)
            logging.info(f"Created and saved scaler to {scaler_path}")
        else:
            # Load existing scaler
            self.scaler = joblib.load(scaler_path)
        
        # Initialize Spotify client
        logging.info("Initializing Spotify client...")
        client_credentials_manager = SpotifyClientCredentials(
            client_id=os.getenv('SPOTIFY_CLIENT_ID', 'cac8b6469aa24671b4566afb16edfc71'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET', 'c197cc5b58a945cf8baa6f9e9bf58cd4')
        )
        self.sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    
    def calculate_diversity_score(self, track_ids):
        """
        Calculate a comprehensive diversity score for a set of tracks
        """
        if not track_ids or len(track_ids) < 2:
            return 0
        
        # Get tracks from our dataset
        tracks = self.tracks_df[self.tracks_df['track_id'].isin(track_ids)]
        
        if len(tracks) < 2:
            # If we don't have enough tracks in our dataset, try to fetch from Spotify
            try:
                # Fetch additional track details from Spotify
                additional_tracks = self.get_track_features(track_ids)
                if len(additional_tracks) >= 2:
                    features = additional_tracks[self.audio_features].values
                    tracks = additional_tracks
                else:
                    return 0
            except Exception as e:
                logging.error(f"Error fetching track features: {e}")
                return 0
        else:
            # Use tracks from our dataset
            features = tracks[self.audio_features].values
        
        # Scale features
        scaled_features = pd.DataFrame(
            self.scaler.transform(features),
            columns=self.audio_features
        )
        
        # Pairwise distance calculation
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
            feature_values = scaled_features[feature_name]
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
    
    def get_track_features(self, track_ids):
        """Fetch track features from Spotify"""
        track_features = []
        for track_id in track_ids:
            try:
                # Fetch track and audio features
                track = self.sp.track(track_id)
                audio_features = self.sp.audio_features(track_id)[0]
                
                # Fetch artist genres
                artist_id = track['artists'][0]['id']
                artist_info = self.sp.artist(artist_id)
                
                # Comprehensive feature extraction
                track_features.append({
                    'track_id': track_id,
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
                    'genres': ', '.join(artist_info.get('genres', [])),
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'valence': audio_features['valence'],
                    'tempo': audio_features['tempo'],
                    'loudness': audio_features['loudness'],
                    'speechiness': audio_features['speechiness'],
                    'acousticness': audio_features['acousticness'],
                    'liveness': audio_features['liveness'],
                    'instrumentalness': audio_features['instrumentalness']
                })
            except Exception as e:
                logging.error(f"Error fetching track features for {track_id}: {e}")
        
        return pd.DataFrame(track_features)

def test_diversity_score():
    logging.info("Starting Diversity Score Calculation Test")
    
    try:
        # Initialize recommendation engine
        dataset_path = os.path.join(project_dir, 'spotify_data_with_instrumentalness.csv')
        recommendation_engine = RecommendationEngine(dataset_path)
        
        # Ensure we have enough tracks in the dataset
        if len(recommendation_engine.tracks_df) < 10:
            logging.error("Not enough tracks in the dataset for testing")
            return
        
        # Select multiple test cases
        test_cases = []
        for _ in range(3):
            # Randomly select multiple tracks (3-5)
            num_tracks = np.random.randint(3, 6)
            sample_tracks = recommendation_engine.tracks_df.sample(num_tracks)['track_id'].tolist()
            test_cases.append(sample_tracks)
        
        # Run tests
        for i, track_ids in enumerate(test_cases, 1):
            logging.info(f"Test Case {i}: Tracks {track_ids}")
            
            try:
                # Fetch track details
                tracks = recommendation_engine.tracks_df[recommendation_engine.tracks_df['track_id'].isin(track_ids)]
                
                # Calculate diversity score
                score = recommendation_engine.calculate_diversity_score(track_ids)
                
                logging.info(f"Diversity Score: {score}")
                
                # Validate score range
                assert 0 <= score <= 100, f"Score {score} is out of range (0-100)"
                
                # Log track details
                logging.info("\nTrack Details:")
                logging.info(tracks[['track_id', 'track_name', 'artist', 'genres']].to_string())
                
                # Log audio features
                logging.info("\nAudio Features:")
                logging.info(tracks[recommendation_engine.audio_features].to_string())
            
            except Exception as case_error:
                logging.error(f"Error in test case {i}: {case_error}")
                logging.exception("Detailed error traceback:")
        
        logging.info("Diversity Score Calculation Test Complete")
    
    except Exception as e:
        logging.error(f"Critical error during testing: {e}")
        logging.exception("Detailed error traceback:")

# Run the test
if __name__ == "__main__":
    test_diversity_score()
