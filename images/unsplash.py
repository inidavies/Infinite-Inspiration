import requests
import os

CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')
BASE_URL = 'https://api.unsplash.com/'

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_images']

# Call this function
def get_images(theme):
    response = request_images(theme)
    processed_info = process_json(response)
    return processed_info

# Description: chandles 
def request_images(theme):
    headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID), 'Accept-Version': 'v1'}
    PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 9}
    r = requests.get(BASE_URL + '/photos/random', params = PARAMS, headers=headers)
    data = r.json()
    return data

def process_json(images_list):
    all_data = []

    for image in images_list:
        image_id = image['id']
        alt_desc = image['alt_description']
        raw_url = image['urls']['raw']
        full_url = image['urls']['full']
        regular_url = image['urls']['regular']
        small_url = image['urls']['small']
        thumb_url = image['urls']['thumb']
        small_s3_url = image['urls']['small_s3']
        photographer_name = image['user']['name']
        photographer_profile_link = image['user']['links']['html']
        current_image = {'id':image_id, 'image_desc':alt_desc, 'raw_url':raw_url, 'full_url':full_url, 'regular_url':regular_url, 'small_url':small_url, 'thumb_url':thumb_url, 'small_s3_url':small_s3_url, 'photographer':photographer_name, 'photographer_profile':photographer_profile_link}
        all_data.append(current_image)
    return all_data