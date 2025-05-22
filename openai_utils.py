import os
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()

# Initialize the OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4.1-nano"

def analyze_user_prompt(user_input):
    """
    Use GPT to extract detailed music parameters from the user input.
    
    Args:
        user_input (str): User's description of their music preferences
        
    Returns:
        tuple: (extracted_data, raw_response)
    """
    system_prompt = (
        "You are a music recommendation assistant. Analyze the user's input and extract detailed Spotify recommendation parameters."
        "\n\nReturn ONLY a valid JSON object with the following structure:"
        "\n{\n"
        "  \"genres\": [list of 1-5 specific music genres mentioned or implied],\n"
        "  \"artists\": [list of specific artists mentioned or implied, empty if none],\n"
        "  \"mood\": {\n"
        "    \"valence\": [float between 0-1, where 0 is sad and 1 is happy],\n"
        "    \"energy\": [float between 0-1, where 0 is calm and 1 is energetic],\n"
        "    \"danceability\": [float between 0-1, optional],\n"
        "    \"acousticness\": [float between 0-1, optional],\n"
        "    \"instrumentalness\": [float between 0-1, optional]\n"
        "  },\n"
        "  \"keywords\": [list of descriptive terms that capture the essence of the request],\n"
        "  \"description\": [a short 1-2 sentence summary of the music style],\n"
        "  \"song_suggestions\": [list of 5-8 specific song suggestions with artist names that match the user's request]\n"
        "}\n\n"
        "Be precise and specific with genres. If the user mentions a specific mood, artist, or genre, include it. "
        "For song suggestions, provide real songs and artists that match the mood, genre, and style requested. "
        "Make sure song titles and artists are accurate and properly capitalized."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=300
    )

    ai_response = response.choices[0].message.content

    # Parse JSON or return fallback
    try:
        extracted = json.loads(ai_response)
        return extracted, ai_response
    except Exception:
        return {
            "genres": ["pop"],
            "mood": {"valence": 0.5, "energy": 0.5},
            "keywords": []
        }, ai_response
