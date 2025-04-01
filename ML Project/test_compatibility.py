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

# Load necessary components
class RecommendationEngine:
    def __init__(self, dataset_path):
        # Load dataset
        logging.info("Loading dataset...")
        self.tracks_df = pd.read_csv(dataset_path)
        
        # Define audio features
        self.audio_features = [
            'danceability', 'energy', 'valence', 
            'tempo', 'loudness', 'speechiness', 
            'acousticness', 'liveness', 'instrumentalness'
        ]
        
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
    
    def calculate_compatibility_score(self, track_ids):
        """
        Calculate a comprehensive compatibility score between tracks
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
        
        # Comprehensive compatibility calculation
        def calculate_feature_compatibility(feature_name):
            """Calculate compatibility for a specific feature"""
            feature_values = scaled_features[feature_name]
            feature_std = np.std(feature_values)
            
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
        
        return round(final_score, 2)
    
    def get_track_features(self, track_ids):
        """Fetch track features from Spotify"""
        track_features = []
        for track_id in track_ids:
            try:
                # Fetch track and audio features
                track = self.sp.track(track_id)
                audio_features = self.sp.audio_features(track_id)[0]
                
                # Comprehensive feature extraction
                track_features.append({
                    'track_id': track_id,
                    'track_name': track['name'],
                    'artist': track['artists'][0]['name'],
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

def test_compatibility_score():
    logging.info("Starting Compatibility Score Calculation Test")
    
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
            # Randomly select 2 unique tracks
            sample_tracks = recommendation_engine.tracks_df.sample(2)['track_id'].tolist()
            test_cases.append(sample_tracks)
        
        # Run tests
        for i, track_ids in enumerate(test_cases, 1):
            logging.info(f"Test Case {i}: Tracks {track_ids}")
            
            try:
                # Fetch track details
                tracks = recommendation_engine.tracks_df[recommendation_engine.tracks_df['track_id'].isin(track_ids)]
                
                # Calculate compatibility score
                score = recommendation_engine.calculate_compatibility_score(track_ids)
                
                logging.info(f"Compatibility Score: {score}")
                
                # Validate score range
                assert 0 <= score <= 100, f"Score {score} is out of range (0-100)"
                
                # Log track details
                logging.info("\nTrack Details:")
                logging.info(tracks[['track_id', 'track_name', 'artist']].to_string())
                
                # Log audio features
                logging.info("\nAudio Features:")
                logging.info(tracks[recommendation_engine.audio_features].to_string())
            
            except Exception as case_error:
                logging.error(f"Error in test case {i}: {case_error}")
                logging.exception("Detailed error traceback:")
        
        logging.info("Compatibility Score Calculation Test Complete")
    
    except Exception as e:
        logging.error(f"Critical error during testing: {e}")
        logging.exception("Detailed error traceback:")

# Run the test
if __name__ == "__main__":
    test_compatibility_score()
