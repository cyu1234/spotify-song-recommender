import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

def get_tracks_from_filters(extracted_data):
    """
    Use Spotify's recommendations API to find tracks based on extracted parameters.
    
    Args:
        extracted_data (dict): Dictionary containing genres, artists, mood, and keywords
        
    Returns:
        list: List of track dictionaries with name, artist, preview_url, and external_url
    """
    try:
        # Extract parameters from the data
        genres = extracted_data.get('genres', [])
        artists = extracted_data.get('artists', [])
        mood = extracted_data.get('mood', {})
        
        # Prepare recommendation parameters
        recommendation_params = {
            'limit': 10,
            'target_valence': mood.get('valence', 0.5),
            'target_energy': mood.get('energy', 0.5)
        }
        
        # Add optional mood parameters if they exist
        if 'danceability' in mood:
            recommendation_params['target_danceability'] = mood['danceability']
        if 'acousticness' in mood:
            recommendation_params['target_acousticness'] = mood['acousticness']
        if 'instrumentalness' in mood:
            recommendation_params['target_instrumentalness'] = mood['instrumentalness']
        
        # Prepare seed parameters
        seed_artists = []
        seed_tracks = []
        
        # If artists are specified, try to find their Spotify IDs
        if artists:
            for artist_name in artists[:2]:  # Limit to 2 artists to leave room for genres
                try:
                    results = sp.search(q=f'artist:"{artist_name}"', type='artist', limit=1)
                    if results['artists']['items']:
                        seed_artists.append(results['artists']['items'][0]['id'])
                except Exception as e:
                    print(f"Error finding artist {artist_name}: {e}")
        
        # Add seed parameters to recommendation params
        if seed_artists:
            recommendation_params['seed_artists'] = seed_artists[:2]  # Max 2 seed artists
        
        # Get available Spotify genres
        try:
            available_genres = sp.recommendation_genre_seeds()['genres']
            print(f"Available Spotify genres: {available_genres}")
        except Exception as e:
            print(f"Error getting genre seeds: {e}")
            available_genres = ['pop', 'rock', 'hip-hop', 'electronic', 'jazz', 'classical', 'r-n-b', 'country']
        
        # Normalize and match genres to available Spotify genres
        valid_genres = []
        for genre in genres:
            # Convert to lowercase and replace spaces with hyphens
            normalized = genre.lower().replace(' ', '-')
            
            # Check if the genre is directly available
            if normalized in available_genres:
                valid_genres.append(normalized)
                continue
                
            # Try to find a close match
            for available in available_genres:
                if normalized in available or available in normalized:
                    valid_genres.append(available)
                    break
        
        # If no valid genres found, add a default genre
        if not valid_genres:
            valid_genres = ['pop']
            
        # Add seed genres (Spotify allows a total of 5 seed entities)
        remaining_seeds = 5 - len(seed_artists) - len(seed_tracks)
        if valid_genres and remaining_seeds > 0:
            recommendation_params['seed_genres'] = valid_genres[:remaining_seeds]
        
        # If we have no seeds at all, use a default genre
        if not ('seed_genres' in recommendation_params or 'seed_artists' in recommendation_params or 'seed_tracks' in recommendation_params):
            recommendation_params['seed_genres'] = ['pop']
        
        # Print recommendation parameters for debugging
        print(f"Recommendation parameters: {recommendation_params}")
        
        # Get recommendations
        try:
            results = sp.recommendations(**recommendation_params)
            print(f"Successfully got {len(results['tracks'])} recommendations")
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            # Try with just a simple genre seed as fallback
            try:
                print("Trying fallback with simple genre seed...")
                results = sp.recommendations(seed_genres=['pop'], limit=10)
                print(f"Fallback successful, got {len(results['tracks'])} tracks")
            except Exception as e2:
                print(f"Fallback also failed: {e2}")
                # Return empty results
                return []
        
        # Process results
        tracks = []
        for item in results['tracks']:
            # Get album image if available
            album_image = None
            if item['album']['images']:
                album_image = item['album']['images'][0]['url']
                
            track_info = {
                "name": item['name'],
                "artist": item['artists'][0]['name'],
                "album": item['album']['name'],
                "preview_url": item['preview_url'],
                "external_url": item['external_urls']['spotify'],
                "image_url": album_image
            }
            tracks.append(track_info)
        
        return tracks
    except Exception as e:
        print("Spotify API error:", str(e))
        return []
