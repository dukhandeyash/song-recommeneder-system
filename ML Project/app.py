from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd
import numpy as np
import os
import datetime
from spotify_utils import SpotifyAPI, RecommendationEngine
from fuzzywuzzy import process

app = Flask(__name__)

# Initialize Spotify API and Recommendation Engine
spotify_api = SpotifyAPI()

# Load processed tracks for local recommendations
def load_processed_tracks():
    try:
        return pd.read_csv('models/processed_tracks.csv')
    except Exception as e:
        print(f"Error loading processed tracks: {e}")
        return None

processed_tracks = load_processed_tracks()

# Check if models directory exists, if not, we need to train the model first
if not os.path.exists('models') or not os.path.exists('models/processed_tracks.csv'):
    print("Models not found. Please run train_model.py first.")
    recommendation_engine = None
else:
    recommendation_engine = RecommendationEngine()

@app.route('/')
def index():
    # Check if models are loaded
    if recommendation_engine is None:
        return render_template('setup.html')
    
    # Get current hour to suggest time-of-day playlists
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        suggested_time = "Morning"
    elif 12 <= current_hour < 17:
        suggested_time = "Afternoon"
    elif 17 <= current_hour < 21:
        suggested_time = "Evening"
    else:
        suggested_time = "Night"
    
    return render_template('index.html', suggested_time=suggested_time)

@app.route('/setup', methods=['POST'])
def setup():
    # This route will be called to train the model
    import subprocess
    subprocess.Popen(['python', 'train_model.py'])
    return jsonify({'status': 'Training started. This may take a few minutes.'})

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if not query:
        return jsonify([])
    
    results = spotify_api.search_tracks(query)
    
    # Format the results
    formatted_results = []
    for track in results:
        image_url = None
        if track['album']['images'] and len(track['album']['images']) > 0:
            image_url = track['album']['images'][0]['url']
        
        formatted_results.append({
            'id': track['id'],
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album': track['album']['name'],
            'image': image_url
        })
    
    return jsonify(formatted_results)

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    track_id = request.args.get('track_id', '')
    
    if not track_id or recommendation_engine is None:
        return jsonify([])
    
    similar_tracks = recommendation_engine.get_similar_tracks(track_id)
    
    return jsonify(similar_tracks)

@app.route('/mood_playlist', methods=['GET'])
def mood_playlist():
    mood = request.args.get('mood', '')
    
    if not mood or recommendation_engine is None:
        return jsonify([])
    
    tracks = recommendation_engine.get_mood_playlist(mood)
    
    return jsonify(tracks)

@app.route('/activity_playlist', methods=['GET'])
def activity_playlist():
    activity = request.args.get('activity', '')
    
    if not activity or recommendation_engine is None:
        return jsonify([])
    
    tracks = recommendation_engine.get_activity_playlist(activity)
    
    return jsonify(tracks)

@app.route('/time_playlist', methods=['GET'])
def time_playlist():
    time_of_day = request.args.get('time', '')
    
    if not time_of_day or recommendation_engine is None:
        return jsonify([])
    
    tracks = recommendation_engine.get_time_of_day_playlist(time_of_day)
    
    return jsonify(tracks)

@app.route('/compatibility', methods=['POST'])
def compatibility():
    data = request.get_json()
    track_ids = data.get('track_ids', [])
    
    if not track_ids or recommendation_engine is None:
        return jsonify({'score': 0})
    
    score = recommendation_engine.calculate_compatibility_score(track_ids)
    
    return jsonify({'score': score})

@app.route('/diversity', methods=['POST'])
def diversity():
    data = request.get_json()
    track_ids = data.get('track_ids', [])
    
    if not track_ids or recommendation_engine is None:
        return jsonify({'score': 0})
    
    score = recommendation_engine.calculate_diversity_score(track_ids)
    
    return jsonify({'score': score})

@app.route('/calculate_diversity_score', methods=['POST'])
def calculate_diversity_score():
    """
    Calculate the diversity score for a given set of tracks
    """
    try:
        # Get track IDs from request
        data = request.get_json()
        track_ids = data.get('track_ids', [])
        
        # Validate input
        if not track_ids or len(track_ids) < 2:
            return jsonify({
                'error': 'Please select at least 2 tracks',
                'diversity_score': 0
            }), 400
        
        # Calculate diversity score using recommendation engine
        diversity_score = recommendation_engine.calculate_diversity_score(track_ids)
        
        # Return diversity score
        return jsonify({
            'diversity_score': diversity_score
        })
    
    except Exception as e:
        # Log the error
        app.logger.error(f"Diversity score calculation error: {str(e)}")
        
        # Return error response
        return jsonify({
            'error': 'Failed to calculate diversity score',
            'details': str(e),
            'diversity_score': 0
        }), 500

@app.route('/local_song_search', methods=['GET'])
def local_song_search():
    """
    Search for songs in the local database using fuzzy matching.
    """
    if processed_tracks is None:
        return jsonify({'error': 'Processed tracks not loaded'})
    
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify([])
    
    # Fuzzy search across track names
    song_names = processed_tracks['track_name'].tolist()
    matches = process.extract(query, song_names, limit=5)  # Limit to 5 results
    
    # Collect matching songs
    results = []
    for match, score in matches:
        if score >= 70:  # 70% similarity threshold
            song_rows = processed_tracks[processed_tracks['track_name'] == match]
            for _, song in song_rows.iterrows():
                results.append({
                    'name': song['track_name'],
                    'artist': song['artist'],
                    'album': song['album'],
                    'mood': song['mood'],
                    'activity': song['activity'],
                    'time_of_day': song['time_of_day']
                })
    
    return jsonify(results)

@app.route('/local_song_recommendations', methods=['GET'])
def local_song_recommendations():
    """
    Get recommendations for a song from the local database.
    """
    if processed_tracks is None:
        return jsonify({'error': 'Processed tracks not loaded'})
    
    song_name = request.args.get('song_name', '').strip()
    if not song_name:
        return jsonify([])
    
    # Find the song in the dataset
    song_row = processed_tracks[processed_tracks['track_name'] == song_name]
    
    if song_row.empty:
        # Use fuzzy matching if exact match not found
        song_names = processed_tracks['track_name'].tolist()
        match = process.extractOne(song_name, song_names)
        
        if match and match[1] >= 80:  # 80% similarity threshold
            song_row = processed_tracks[processed_tracks['track_name'] == match[0]]
        else:
            return jsonify({'error': 'Song not found'})
    
    # Get the first matching song
    base_song = song_row.iloc[0]
    
    # Find similar songs based on mood and activity
    similar_songs = processed_tracks[
        (processed_tracks['mood'] == base_song['mood']) | 
        (processed_tracks['activity'] == base_song['activity'])
    ]
    
    # Exclude the base song
    similar_songs = similar_songs[similar_songs['track_name'] != base_song['track_name']]
    
    # Take top 5 recommendations
    recommendations = similar_songs.head(5)
    
    results = []
    for _, song in recommendations.iterrows():
        results.append({
            'name': song['track_name'],
            'artist': song['artist'],
            'album': song['album'],
            'mood': song['mood'],
            'activity': song['activity'],
            'time_of_day': song['time_of_day']
        })
    
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)