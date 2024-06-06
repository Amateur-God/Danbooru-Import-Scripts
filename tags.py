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

def retrieve_my_site_tags(my_site_session):
    base_url = f"{YOUR_DANBOORU_SITE}/tags.json"
    all_tags = []
    page = 1
    page_limit = 1000  # Set the page limit to 1000
    
    while True:
    #while page <= page_limit:
        response = my_site_session.get(f"{base_url}?page={page}&limit=100")  # Assuming 100 tags per page
        if response.status_code == 200:
            tags = response.json()
            if not tags:  # No more tags to fetch
                break
            all_tags.extend(tags)
            print(f"Processing tag page {page}")
            page += 1
        else:
            print(f"Error retrieving tags from my_site: {response.status_code}")
            break
    
    return all_tags


def search_danbooru_for_tag(danbooru_session, tag_name):
    response = danbooru_session.get(f"https://danbooru.donmai.us/tags.json?search[name]={tag_name}")
    if response.status_code == 200 and response.json():
        return response.json()[0]
    else:
        return None

def update_my_site_tag(my_site_session, tag, danbooru_tag_info):
    if danbooru_tag_info:
        update_url = f"{YOUR_DANBOORU_SITE}/tags/{tag['id']}.json"
        # Update the tag's category based on Danbooru's tag info
        data = {
            "tag": {
                "category": danbooru_tag_info.get("category")
            }
        }
        response = my_site_session.put(update_url, json=data)
        if response.status_code in [200, 204]:
            print(f"Updated tag {tag['name']} successfully.")
        else:
            print(f"Failed to update tag {tag['name']}: {response.status_code}, Response: {response.text}")


def main():
    danbooru_session = login_with_api_key_danbooru(DANBOORU_USERNAME, DANBOORU_API_KEY)
    my_site_session = login_with_api_key_my_site(SITE_USERNAME, SITE_API_KEY)

    my_site_tags = retrieve_my_site_tags(my_site_session)
    for tag in my_site_tags:
        danbooru_tag_info = search_danbooru_for_tag(danbooru_session, tag['name'])
        update_my_site_tag(my_site_session, tag, danbooru_tag_info)

if __name__ == "__main__":
    main()
