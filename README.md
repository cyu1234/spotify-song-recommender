# Spotify Song Suggester with AI

A web application that suggests songs based on user inputs using Spotify's API and OpenAI's API.

## Features

- Search for tracks by artist name
- Find similar artists
- Get song recommendations based on mood (valence and energy)
- AI-powered recommendations based on natural language descriptions
- Beautiful Spotify-inspired UI

## Setup

1. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set up environment variables (optional):
   - Create a `.env` file in the project root with the following variables:
   ```
   SPOTIFY_CLIENT_ID=your_spotify_client_id
   SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
   OPENAI_API_KEY=your_openai_api_key
   ```
   - Or set these variables directly in the code (spotify_utils.py and openai_utils.py)

3. Run the application:
   ```
   python app.py
   ```

4. Open your browser and navigate to:
   ```
   http://127.0.0.1:8888
   ```

## How It Works

1. **Artist Search**: Enter an artist name to find their top tracks
2. **Similar Artists**: Find artists similar to your favorite artists
3. **Mood-Based**: Select a genre and adjust mood sliders to get recommendations
4. **AI-Powered**: Describe what you're looking for in natural language, and the AI will analyze your preferences and suggest appropriate music

## Technologies Used

- Flask: Web framework
- Spotify API: Music data and recommendations
- OpenAI API: Natural language processing for music preferences
- Bootstrap: UI components and styling
- JavaScript: Frontend interactivity
