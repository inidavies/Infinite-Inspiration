import requests
import os

CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')
BASE_URL = 'https://api.unsplash.com/'

# Call this function
def get_images(theme):
    theme = input('Enter your desired theme: ')
    response = request_images(theme)
    processed_info = process_json(response)
    return processed_info

# Don't call any of these
def request_images(theme):
    headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID), 'Accept-Version': 'v1'}
    PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 1}
    r = requests.get(BASE_URL + '/photos/random', params = PARAMS, headers=headers)
    data = r.json()
    return data

def process_json(images_list):
    all_data = []

    for image in images_list:
        image_id = image['id']
        alt_desc = image['alt_description']
        urls = image['urls']
        photographer = image['user']['name']
        profile_link = image['user']['links']['html']
        current_image = {'id':image_id, 'image_desc':alt_desc, 'urls':urls, 'photographer':photographer, 'photographer_profile':profile_link}
        all_data.append(current_image)
    return all_data
