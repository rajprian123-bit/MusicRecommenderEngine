import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('LASTFM_API_KEY')


GENRE_MAP = {
    'rap': ['trap', 'drill', 'conscious hip-hop', 'gangsta rap', 'cloud rap'],
    'rock': ['indie rock', 'alternative', 'classic rock', 'psychedelic rock', 'punk'],
    'pop': ['k-pop', 'indie pop', 'dance pop', 'synthpop', 'hyperpop'],
    'electronic': ['house', 'techno', 'dubstep', 'drum and bass', 'ambient'],
    'jazz': ['bebop', 'smooth jazz', 'swing', 'fusion'],
    'r&b': ['neo-soul', 'soul', 'contemporary r&b', 'funk'],
    'metal': ['heavy metal', 'black metal', 'deathcore', 'thrash metal']
}



def get_manual_subgenres(base_tag):
    base_tag = base_tag.lower()
    return GENRE_MAP.get(base_tag)

def get_tracks_by_tag(tag):
    output = ""  
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'tag.gettoptracks',
        'tag': tag,
        'api_key': API_KEY,
        'limit': 20,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            
            if 'tracks' in data and 'track' in data['tracks']:
                list_of_songs = data['tracks']['track']
                output += f"\nTop tracks for: {tag.upper()}\n"
                for song in list_of_songs:
                    title = song['name']
                    if 'artist' in song and 'name' in song['artist']:
                        artist = song['artist']['name']
                        output += f"- {title} by {artist}\n"
            else:
                output += "No tracks found for this tag.\n"
        else:
            output += f"Error: API returned status code {response.status_code}\n"
            
    except Exception as e:
        output += f"Network error: {e}\n"
        
    return output  

def get_similar_tracks(artist_name):
    output = f"\nLooking for artists similar to {artist_name}...\n"
    
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'artist.getsimilar',
        'artist': artist_name,
        'api_key': API_KEY,
        'format': 'json',
        'limit': 5,
        'autocorrect': 1
    }

    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json() 

            if 'similarartists' in data and 'artist' in data['similarartists']:
                artists = data['similarartists']['artist']
            
                if not artists:
                    return "No similar artists found.\n"

                output += f"\n🎧 If you like {artist_name}, you might like:\n"
                
                for i, artist_obj in enumerate(artists):
                    similar_artist = artist_obj['name']
                    output += f"\n{i+1}. {similar_artist}\n"
                    output += get_top_track_for_artist(similar_artist)    
            else:
                output += "Could not find that artist.\n"   
        else:
            output += f"Error: API returned status code {response.status_code}\n"
    except Exception as e:
        output += f"Network error: {e}\n"
        
    return output

def get_top_track_for_artist(artist_name):
    output = ""
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'artist.gettoptracks',
        'artist': artist_name,
        'api_key': API_KEY,
        'limit': 1, 
        'format': 'json'
    }
    
    try:
        r = requests.get(url, params=params)
        d = r.json()
        if 'toptracks' in d and 'track' in d['toptracks']:
            tracks = d['toptracks']['track']
            if isinstance(tracks, list) and len(tracks) > 0:
                output = f"   ↳ Recommended: {tracks[0]['name']}\n"
    except:
        pass 
    return output

def get_current_hits():
    output = "\nFetching Top Current Songs via Last.fm...\n"
    
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'chart.gettoptracks',
        'api_key': API_KEY,
        'limit': 10, 
        'format': 'json'
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'tracks' in data and 'track' in data['tracks']:
                currenthits = data['tracks']['track']
                output += "\nTop 10 Trending on Last.fm:\n"
                for i, t in enumerate(currenthits):
                    title = t['name']
                    artist = t['artist']['name'] 
                    output += f"{i+1}. {title} by {artist}\n"
            else:
                output += "Chart data not found.\n"
        else:
            output += f"Error: {response.status_code}\n"
            
    except Exception as e:
        output += f"Network error: {e}\n"
    return output

def get_albums_by_genre(tag):
    output = ""
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'tag.gettopalbums', 
        'tag': tag,
        'api_key': API_KEY,
        'limit': 10,
        'format': 'json'
    }
    
    try:
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if 'albums' in data and 'album' in data['albums']:
                albums = data['albums']['album']
                
                output += f"\nTop {tag.title()} Albums:\n"
                for i, album in enumerate(albums):
                    title = album['name']
                    artist = album['artist']['name']
                    output += f"{i+1}. {title} by {artist}\n"
            else:
                output += "No albums found for this genre.\n"
        else:
            output += f"Error: {response.status_code}\n"
            
    except Exception as e:
        output += f"Network error: {e}\n"
    return output

def get_top_albums(artist):
    output = ""
    url = "http://ws.audioscrobbler.com/2.0/"
    params = {
        'method': 'artist.gettopalbums',
        'api_key': API_KEY,
        'limit': 5,  
        'artist': artist,
        'format': 'json',
        'autocorrect': 1
    }
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'topalbums' in data and 'album' in data['topalbums']:
                albums = data['topalbums']['album']
                output += f"\nTop Albums by {artist.title()}:\n"
                for i, album in enumerate(albums):
                    title = album['name']
                    plays = album.get('playcount', 'N/A') 
                    output += f"{i+1}. {title}\n"
            else:
                output += "Artist or albums not found.\n"
        else:
            output += f"Error: {response.status_code}\n"
            
    except Exception as e:
        output += f"Network error: {e}\n"
    return output

if __name__ == "__main__":
    print("\n --- Music Recommender Engine ---")
    if not API_KEY:
        print("WARNING: API Key not found!")
        
    while True:
        print("\n" + "="*40)
        category = input("Are you looking for (S)ongs or (A)lbums? (or 'exit'): ").lower().strip()

        if category == 'exit':
            print("Exiting...")
            break

        elif category.startswith('s'):
            print("\n🎵 --- SONG MODE ---")
            mode = input("Search by (G)enre, (S)imilar to a song, or (C)harts? ").lower().strip()
            
            if mode.startswith('g'):
                tag = input("Enter a Genre: ").strip()
                possible_subs = get_manual_subgenres(tag)
                if possible_subs:
                    print(f"   Options: {possible_subs}")
                    refinement = input("   Type a sub-genre (or Enter to skip): ").strip()
                    if refinement: tag = refinement
                print(get_tracks_by_tag(tag))
                
            elif mode.startswith('s'):
                artist = input("Enter an Artist you like: ").strip()
                print(get_similar_tracks(artist))
                
            elif mode.startswith('c'):
                print(get_current_hits())
                
            else:
                print("Invalid song command.")

        elif category.startswith('a'):
            print("\n💿 --- ALBUM MODE ---")
            mode = input("Search by (G)enre or (A)rtist? ").lower().strip()
            
            if mode.startswith('a'):
                artist = input("Enter the Artist: ").strip()
                print(get_top_albums(artist))
            
            elif mode.startswith('g'):
                tag = input("Enter a Genre (e.g. Rap, Jazz): ").strip()
                possible_subs = get_manual_subgenres(tag)
                if possible_subs:
                    print(f"   Options: {possible_subs}")
                    refinement = input("   Type a sub-genre (or Enter to skip): ").strip()
                    if refinement: tag = refinement
                
                print(get_albums_by_genre(tag))
            
            else:
                print("Invalid album command.")

        else:
            print("Please type 's' for Songs or 'a' for Albums.")