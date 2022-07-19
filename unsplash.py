import requests
import os

CLIENT_ID = os.environ.get('UNSPLASH_CLIENT_ID')
CLIENT_SECRET = os.environ.get('UNSPLASH_CLIENT_SECRET')

headers = {'Authorization': 'Client-ID {token}'.format(token=CLIENT_ID), 'Accept-Version': 'v1'}

BASE_URL = 'https://api.unsplash.com/'
theme = input('Enter your desired theme: ')
PARAMS = {'query': theme, 'orientation': 'landscape', 'count': 2}
r = requests.get(BASE_URL + '/photos/random', params = PARAMS, headers=headers)
data = r.json()
print(data)