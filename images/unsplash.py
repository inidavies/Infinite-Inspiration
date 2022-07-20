import requests
import os

CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')
BASE_URL = 'https://api.unsplash.com/'

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_images']

# Call this function
def get_images():
    theme = input('Enter your desired theme: ')
    response = request_images(theme)
    processed_info = process_json(response, theme)
    return processed_info

# Description: chandles 
def request_images(theme):
    headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID), 'Accept-Version': 'v1'}
    PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 9}
    r = requests.get(BASE_URL + '/photos/random', params = PARAMS, headers=headers)
    data = r.json()
    return data

def process_json(images_list, theme):
    all_data = []

    for image in images_list:
        image_id = image['id']
        alt_desc = image['alt_description']
        regular_url = image['urls']['regular']
        thumb_url = image['urls']['thumb']
        photographer_name = image['user']['name']
        photographer_profile_link = image['user']['links']['html']
        current_image = {'theme':theme, 'id':image_id, 'image_desc':alt_desc, 'regular_url':regular_url, 'thumb_url':thumb_url, 'photographer':photographer_name, 'photographer_profile':photographer_profile_link}
        all_data.append(current_image)
    return all_data
