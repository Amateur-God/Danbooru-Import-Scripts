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

def retrieve_artist_by_id(session, artist_id):
    base_url = f"https://danbooru.donmai.us/artists/{artist_id}.json"
    response = session.get(base_url)
    if response.status_code == 200:
        artist = response.json()
        formatted_artist = {
            "id": artist["id"],
            "name": artist.get("name", ""),
            "other_names": artist.get("other_names", []),
            "group_name": artist.get("group_name", ""),
            "urls": retrieve_artist_urls(artist["id"], session)  # Pass session here
        }
        return formatted_artist
    else:
        print(f"Error retrieving artist with ID {artist_id}: {response.status_code}")
        return None


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


def upload_artist(artist, session):
    if artist:  # Proceed only if the artist data was successfully retrieved
        create_url = f"{YOUR_DANBOORU_SITE}/artists.json"
        data = {
            "artist": {
                "name": artist["name"],
                "other_names": ", ".join(artist.get("other_names", [])),
                "group_name": artist.get("group_name", ""),
                "url_string": "\n".join(artist.get("urls", [])),  # Correctly join URLs with newlines
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
    search_url = f"{YOUR_DANBOORU_SITE}/artists.json?search[name]={artist_name}"
    response = session.get(search_url)
    if response.status_code == 200 and response.json():
        artist = response.json()[0]
        return True, artist["id"]
    return False, None


def main():

    danbooru_session = login_with_api_key_danbooru(DANBOORU_USERNAME, DANBOORU_API_KEY)
    my_site_session = login_with_api_key_my_site(SITE_USERNAME, SITE_API_KEY)

    try:
        while True:
            artist_id = input("Enter the artist ID to search for (or press Ctrl+C to exit): ")
            if not artist_id:
                print("Artist ID cannot be empty. Please try again.")
                continue

            # Retrieve artists using Danbooru session
            artist = retrieve_artist_by_id(danbooru_session, artist_id)
            
            # Upload artists using my_site session
            upload_artist(artist, my_site_session)
    except KeyboardInterrupt:
        print("\nExiting the program.")
if __name__ == "__main__":
    main()

