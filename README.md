# Spotify AI Music Discovery

A web application that generates personalized music recommendations using natural language processing with OpenAI's GPT-4.1-nano model and the Spotify API.

## Features

- **AI-Powered Music Discovery**: Describe your mood, preferences, or the type of music you're looking for in natural language
- **Intelligent Analysis**: The application uses GPT-4.1-nano to extract musical parameters from your description
- **Personalized Recommendations**: Get Spotify track recommendations based on:
  - Mood parameters (valence, energy, danceability, etc.)
  - Genre preferences
  - Artist influences
- **Dual Recommendation System**:
  - AI-suggested songs with artist names
  - Actual Spotify tracks with preview links
- **Beautiful Responsive UI**:
  - Dark/light mode toggle
  - Spotify-inspired design
  - Mobile-friendly layout

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   - Create a `.env` file in the project root with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8888
   ```

## How It Works

1. **User Input**: You describe what kind of music you're looking for in natural language
   - Example: "I'm feeling down today and need some uplifting music that isn't too energetic. I usually like indie folk and acoustic songs."

2. **AI Analysis**: The OpenAI GPT-4.1-nano model analyzes your request and extracts:
   - Relevant genres
   - Artist influences (if mentioned)
   - Mood parameters (valence, energy, danceability, etc.)
   - Specific song suggestions

3. **Spotify API Integration**: The application uses the extracted parameters to:
   - Find matching genres in Spotify's available genre seeds
   - Search for artist IDs if artists were mentioned
   - Set appropriate mood parameters (valence, energy, etc.)
   - Request personalized recommendations from Spotify

4. **Results Display**: The application presents:
   - A custom playlist title and description
   - AI-suggested songs with links to search for them on Spotify
   - Spotify track recommendations with album art, preview links, and direct Spotify links
   - Analysis of the extracted musical parameters

## Technologies Used

- **Backend**:
  - Flask: Web framework for the API
  - Python 3: Core programming language
  - OpenAI API: Natural language processing (GPT-4.1-nano model)
  - Spotipy: Python library for the Spotify Web API

- **Frontend**:
  - HTML5/CSS3: Structure and styling
  - JavaScript: Dynamic content and API interactions
  - Bootstrap 5: Responsive UI components
  - Font Awesome: Icons

- **APIs**:
  - Spotify Web API: Music recommendations and track information
  - OpenAI API: Natural language processing

## Example Use Cases

- Finding music that matches your current mood
- Discovering songs similar to a specific artist or genre
- Creating themed playlists based on activities or occasions
- Exploring new genres with guidance from AI
