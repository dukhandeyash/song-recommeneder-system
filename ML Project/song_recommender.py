import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
from fuzzywuzzy import process

class SongRecommender:
    def __init__(self, processed_tracks_path='models/processed_tracks.csv'):
        """
        Initialize the song recommender with pre-processed data and models.
        
        Args:
            processed_tracks_path (str): Path to the processed tracks CSV file
        """
        # Load processed tracks
        self.tracks_df = pd.read_csv(processed_tracks_path)
        
        # Load pre-trained models
        self.scaler = joblib.load('models/scaler.pkl')
        self.nn_model = joblib.load('models/nearest_neighbors.pkl')
        
        # Audio features used for recommendation
        self.audio_features = [
            'danceability', 'energy', 'valence', 'tempo', 'loudness', 
            'speechiness', 'acousticness', 'liveness', 'instrumentalness'
        ]
        
        # Precompute song names for faster fuzzy matching
        self.song_names = self.tracks_df['track_name'].tolist()
    
    def find_closest_song(self, input_song):
        """
        Find the closest matching song in the database using fuzzy matching.
        
        Args:
            input_song (str): Song name to match
        
        Returns:
            Matched song row or None
        """
        # Use fuzzy matching to find the closest song name
        match = process.extractOne(input_song, self.song_names)
        
        if match and match[1] >= 80:  # 80% similarity threshold
            matched_song = match[0]
            song_row = self.tracks_df[self.tracks_df['track_name'] == matched_song]
            return song_row
        
        return None
    
    def get_song_recommendations(self, song_name, top_n=5):
        """
        Get similar song recommendations based on audio features.
        
        Args:
            song_name (str): Name of the song to find similar songs for
            top_n (int): Number of recommendations to return
        
        Returns:
            DataFrame of recommended songs
        """
        # Find the song in the dataset using fuzzy matching
        song_row = self.find_closest_song(song_name)
        
        if song_row is None or song_row.empty:
            print(f"No close match found for song '{song_name}'.")
            return None
        
        # Extract features for the selected song
        song_features = song_row[self.audio_features].values
        
        # Scale the features
        song_features_scaled = self.scaler.transform(song_features)
        
        # Find nearest neighbors
        distances, indices = self.nn_model.kneighbors(song_features_scaled, n_neighbors=top_n+1)
        
        # Get recommended songs (excluding the input song itself)
        recommended_indices = indices[0][1:]
        recommended_songs = self.tracks_df.iloc[recommended_indices]
        
        # Print the matched song
        print(f"Matched Song: {song_row['track_name'].values[0]} by {song_row['artist'].values[0]}")
        
        return recommended_songs[['track_name', 'artist', 'album', 'mood', 'activity', 'time_of_day']]
    
    def search_songs(self, query, top_matches=10):
        """
        Search for songs by partial name or artist.
        
        Args:
            query (str): Search term
            top_matches (int): Number of matches to return
        
        Returns:
            DataFrame of matching songs
        """
        # Fuzzy search across track names and artists
        track_matches = process.extract(query, self.song_names, limit=top_matches)
        
        # Collect matching songs
        matched_songs = []
        for match, score in track_matches:
            if score >= 70:  # 70% similarity threshold
                song_rows = self.tracks_df[self.tracks_df['track_name'] == match]
                matched_songs.append(song_rows)
        
        if matched_songs:
            return pd.concat(matched_songs)[['track_name', 'artist']]
        else:
            print("No matching songs found.")
            return None

def main():
    # Create recommender instance
    recommender = SongRecommender()
    
    print("Song Recommendation System")
    print("Commands:")
    print("- 'search <query>': Find songs")
    print("- 'recommend <song>': Get recommendations")
    print("- 'quit': Exit the program")
    
    while True:
        user_input = input("\nEnter a command: ").strip()
        
        if user_input.lower() == 'quit':
            break
        
        # Search for songs
        if user_input.lower().startswith('search '):
            query = user_input[7:]
            results = recommender.search_songs(query)
            if results is not None:
                print(results)
        
        # Get recommendations
        elif user_input.lower().startswith('recommend '):
            song_name = user_input[10:]
            recommendations = recommender.get_song_recommendations(song_name)
            
            if recommendations is not None:
                print("\nRecommended Songs:")
                print(recommendations)
        
        else:
            print("Invalid command. Use 'search', 'recommend', or 'quit'.")

if __name__ == "__main__":
    main()
