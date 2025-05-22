from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv
import os
import openai_utils
import spotify_utils

load_dotenv()
app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ai_recommendation', methods=['POST'])
def ai_recommendation():
    user_input = request.form.get('user_input', '')
    if not user_input:
        return jsonify({'error': 'No input provided'}), 400

    try:
        # Step 1: Use OpenAI to analyze input and extract music parameters
        extracted_data, raw_response = openai_utils.analyze_user_prompt(user_input)
        
        # Print the extracted data for debugging
        print(f"Extracted data: {extracted_data}")
        
        # Step 2: Use Spotify API to find tracks based on the extracted parameters
        tracks = spotify_utils.get_tracks_from_filters(extracted_data)
        
        # Generate a description using the extracted data
        custom_description = extracted_data.get('description', '')
        genres_text = ', '.join(extracted_data.get('genres', [])[:3])
        artists_text = ', '.join(extracted_data.get('artists', [])[:2])
        
        # Create a formatted description
        if custom_description:
            description = f"PLAYLIST TITLE: {custom_description.split('.')[0]}\n\n{custom_description}"
        else:
            description = f"PLAYLIST TITLE: Your Custom Mix\n\nA playlist featuring {genres_text} music"
            if artists_text:
                description += f" inspired by {artists_text}"
            description += "."
        
        # Get song suggestions from OpenAI response
        ai_song_suggestions = extracted_data.get('song_suggestions', [])
        
        # Respond with payload (excluding raw OpenAI response)
        return jsonify({
            "description": description,
            "spotify_tracks": tracks,
            "ai_song_suggestions": ai_song_suggestions,
            "ai_response": extracted_data,
            "user_input": user_input
        })
    except Exception as e:
        print("Error in recommendation:", e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8888)
