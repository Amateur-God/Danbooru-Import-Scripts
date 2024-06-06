from dotenv import load_dotenv
import requests
import os

env_file = 'config/config.env'
load_dotenv(dotenv_path=env_file)

YOUR_DANBOORU_SITE = os.getenv('YOUR_DANBOORU_SITE')
# Credentials for Danbooru
DANBOORU_USERNAME = os.getenv('DANBOORU_USERNAME')
DANBOORU_API_KEY = os.getenv('DANBOORU_API_KEY')
# Credentials for Your Site
SITE_USERNAME = os.getenv('SITE_USERNAME')
SITE_API_KEY = os.getenv('SITE_API_KEY')

def login_with_api_key_danbooru(username, api_key):
    session = requests.Session()
    session.auth = (username, api_key)
    print("Login to Danbooru successful.")
    return session

def login_with_api_key_my_site(username, api_key):
    session = requests.Session()
    session.auth = (username, api_key)
    print("Login to my_site successful.")
    return session

def retrieve_artists(session):
    base_url = "https://danbooru.donmai.us/artists.json"
    all_artists = []
    page = 1
    page_limit = 1000 # Adjusted for demonstration

    while page <= page_limit:
        response = session.get(f"{base_url}?page={page}")
        if response.status_code == 200:
            artists = response.json()
            if not artists:
                break
            all_artists.extend(artists)
            print(f"Processing artist page {page}")
            page += 1
        else:
            print(f"Error retrieving artists: {response.status_code}")
            break

    formatted_artists = []
    for artist in all_artists:
        formatted_artist = {
            "id": artist["id"],
            "name": artist.get("name", ""),
            "other_names": artist.get("other_names", []),
            "group_name": artist.get("group_name", ""),
            "urls": retrieve_artist_urls(artist["id"], session)  # Pass session here
        }
        formatted_artists.append(formatted_artist)
    return formatted_artists

def retrieve_artist_urls(artist_id, session):
    base_url = "https://danbooru.donmai.us/artist_urls.json"
    urls = []
    page = 1

    while True:
        response = session.get(f"{base_url}?search[artist_id]={artist_id}&page={page}")
        if response.status_code == 200:
            artist_urls = response.json()
            if not artist_urls:  # If no more URLs, break the loop
                break
            for url_info in artist_urls:
                urls.append(url_info["url"])
                print(f"Processing artist {artist_id}, URL: {url_info['url']}")
            page += 1
        else:
            print(f"Error retrieving URLs for artist ID {artist_id}: {response.status_code}")
            break
    
    return urls

def upload_artists(artists, session):
    create_url = f"{YOUR_DANBOORU_SITE}/artists.json"
    for artist in artists:
        # Ensure URLs are joined by actual newline characters
        url_string = "\n".join(artist.get("urls", []))  # Use "\n" for actual newlines

        data = {
            "artist": {
                "name": artist["name"],
                "other_names": ", ".join(artist.get("other_names", [])),
                "group_name": artist.get("group_name", ""),
                "url_string": url_string,  # Now correctly formatted with newlines
            }
        }

        exists, artist_id = check_artist_exists_and_get_id(artist["name"], session)
        if exists:
            update_url = f"{YOUR_DANBOORU_SITE}/artists/{artist_id}.json"
            response = session.put(update_url, json=data)
            action = "updated"
        else:
            response = session.post(create_url, json=data)
            action = "uploaded"

        if response.status_code in [200, 201, 204]:
            print(f"Successfully {action} artist: {artist['name']}")
        else:
            print(f"Error {action} artist {artist['name']}: {response.text}")


def check_artist_exists_and_get_id(artist_name, session):
    search_url = f"{YOUR_DANBOORU_SITE}/artists.json?search[name]=" + artist_name
    response = session.get(search_url)
    if response.status_code == 200 and response.json():
        artist = response.json()[0]
        return True, artist["id"]
    return False, None

def main():
    # Credentials for Danbooru
    danbooru_session = login_with_api_key_danbooru(DANBOORU_USERNAME, DANBOORU_API_KEY)
    my_site_session = login_with_api_key_my_site(SITE_USERNAME, SITE_API_KEY)

    # Retrieve artists using Danbooru session
    artists = retrieve_artists(danbooru_session)  # Adjust function to accept session parameter

    # Upload artists using my_site session
    upload_artists(artists, my_site_session)  # Adjust function to accept session parameter

if __name__ == "__main__":
    main()

