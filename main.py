import os
import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# API Keys
LASTFM_API_KEY = os.getenv('LASTFM_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=OPENAI_API_KEY)

# --- LOCAL FALLBACK DATA (Your original logic) ---
GENRE_MAP = {
    'rap': ['trap', 'drill', 'conscious hip-hop'],
    'rock': ['indie rock', 'alternative', 'classic rock'],
    'pop': ['k-pop', 'indie pop', 'synthpop'],
    'electronic': ['house', 'techno', 'ambient'],
    'jazz': ['bebop', 'smooth jazz', 'fusion'],
    'r&b': ['neo-soul', 'soul', 'funk'],
    'metal': ['heavy metal', 'black metal', 'thrash metal']
}

def get_fallback_tags(user_input):
    """
    Standard keyword matching if the AI fails.
    """
    user_input = user_input.lower()
    for key in GENRE_MAP:
        if key in user_input:
            return GENRE_MAP[key]
    return ["rock", "pop", "electronic"] # Absolute baseline

# --- AI INTEGRATION LAYER ---

def get_ai_refined_tags(user_input):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Translate user mood into 3 Last.fm genre tags. Output ONLY tags separated by commas."},
                {"role": "user", "content": user_input}
            ],
            timeout=5 # Don't let the app hang forever
        )
        tags = response.choices[0].message.content.strip().split(", ")
        return [t.strip().lower() for t in tags]
    except Exception as e:
        print(f"\n⚠️ AI Offline. Switching to Local Fallback Logic...")
        return get_fallback_tags(user_input)

# --- DATA FETCHING LAYER (Original Functions) ---

def get_tracks_by_tag(tag):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {'method': 'tag.gettoptracks', 'tag': tag, 'api_key': LASTFM_API_KEY, 'limit': 10, 'format': 'json'}
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'tracks' in data and 'track' in data['tracks']:
                tracks = data['tracks']['track']
                output = f"\n--- {tag.upper()} TOP TRACKS ---\n"
                for song in tracks:
                    output += f"- {song['name']} by {song['artist']['name']}\n"
                return output
    except: return ""
    return ""

def get_albums_by_genre(tag):
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {'method': 'tag.gettopalbums', 'tag': tag, 'api_key': LASTFM_API_KEY, 'limit': 5, 'format': 'json'}
    try:
        r = requests.get(url, params=params).json()
        albums = r['albums']['album']
        output = f"\n💿 Top {tag.title()} Albums:\n"
        for i, a in enumerate(albums):
            output += f"{i+1}. {a['name']} by {a['artist']['name']}\n"
        return output
    except: return ""

def get_current_hits():
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {'method': 'chart.gettoptracks', 'api_key': LASTFM_API_KEY, 'limit': 10, 'format': 'json'}
    try:
        r = requests.get(url, params=params).json()
        tracks = r['tracks']['track']
        output = "\n🔥 Trending Right Now:\n"
        for i, t in enumerate(tracks):
            output += f"{i+1}. {t['name']} by {t['artist']['name']}\n"
        return output
    except: return "Error fetching charts."

# --- MAIN CONTROL ---

if __name__ == "__main__":
    print("\n--- HYBRID MUSIC DISCOVERY ENGINE ---")
    
    while True:
        query = input("\nDescribe your vibe or artist (or 'exit'): ").strip()
        if query.lower() == 'exit': break
        
        mode = input("Looking for (S)ongs, (A)lbums, or (C)harts? ").lower().strip()
        
        if mode.startswith('c'):
            print(get_current_hits())
            continue

        # The Hybrid logic: AI first, Fallback second
        tags = get_ai_refined_tags(query)
        print(f"🏷️  Keywords: {', '.join(tags)}")

        final_output = ""
        for tag in tags:
            if mode.startswith('s'):
                final_output += get_tracks_by_tag(tag)
            elif mode.startswith('a'):
                final_output += get_albums_by_genre(tag)
        
        print(final_output if final_output else "No results found.")