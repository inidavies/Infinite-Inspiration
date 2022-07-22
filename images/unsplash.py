import requests
import os

CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')
BASE_URL = 'https://api.unsplash.com/'

# defining import * for the __init__.py file (to obscure other functions)
__all__ = ['get_images']


# Call this function
def get_images(theme):
    """
    Accesses other functions in order to get data from API
    """
    response = request_images(theme)

    if type(response) is list:
        processed_info = process_json(response, theme)
        return processed_info
    else:
        return -1


def request_images(theme):
    """
    Executes API request
    """
    headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID),
               'Accept-Version': 'v1'}
    PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 9}
    r = requests.get(BASE_URL + '/photos/random',
                     params=PARAMS, headers=headers, timeout=30)
    if r.status_code == 200:
        data = r.json()
        return data
    else:
        str(r.status_code) + ': ' + str(r.reason)


def process_json(images_list, theme):
    """
    Extracts desired data from API response
    """
    all_data = []

    for image in images_list:
        image_id = image['id']
        alt_desc = image['alt_description']
        regular_url = image['urls']['regular']
        thumb_url = image['urls']['thumb']
        photographer_name = image['user']['name']
        photographer_profile_link = image['user']['links']['html']
        current_image = {'theme': theme, 'id': image_id,
                         'image_desc': alt_desc, 'regular_url': regular_url,
                         'thumb_url': thumb_url,
                         'photographer': photographer_name,
                         'photographer_profile': photographer_profile_link}
        all_data.append(current_image)
    return all_data
