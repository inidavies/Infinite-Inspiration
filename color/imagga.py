import os
import random
import requests

# https://docs.imagga.com/#colors to get color from picture
# https://www.thecolorapi.com/docs to get light enough version of the
# color to be suitable for background
# Important info: doesn't work on goo.gl urls but does work on shortened urls (tinyurls)

#defining import * for the __init__.py file (to obscure all other functions)
__all__ = ['background_color']

# API keys and urls
imagga_api_key = os.environ.get('IMAGGA_CLIENT_KEY')
imagga_api_secret = os.environ.get('IMAGGA_CLIENT_SECRET')
imagga_color_url = 'https://api.imagga.com/v2/colors?image_url='
the_color_api_scheme_url = 'https://www.thecolorapi.com/scheme?hex='

# USE THIS TO CALL IN OTHER LOCATIONS
# Description: driver for the imagga and The Color API interaction
# Input: image url (from wherever you are currently working)
# Output: Returns a dictionary with 2 elements: dark (darker color hex code)
# and light (lighter color hex code) -1 if bad url
def background_color(img_url):
    response = get_json_response_imagga(img_url)
    if type(response) is not str:
        processed_response = process_json_response(response)
        color = pick_color(processed_response)
        color_scheme = get_json_response_color_scheme(color)
        final_colors = process_json_response_color_scheme(color_scheme)
        darkest = final_colors['dark']

        while len(final_colors) is 3:
            color_scheme = get_json_response_color_scheme(final_colors['light'])
            final_colors = process_json_response_color_scheme(color_scheme)

        final_colors['dark'] = darkest

        return final_colors
    else:
        return -1

# DO NOT USE ANY OF THE FUNCTIONS BELOW THIS LINE FOR ANYTHING OUTSIDE OF THIS SCRIPT
# Description: handles the api call to imagga
# Input: takes the image url as input
# Output: returns the response in json format
def get_json_response_imagga(img_url):
    response = -1
    try:
        response = requests.get(imagga_color_url + img_url, auth=(imagga_api_key, imagga_api_secret), timeout=15)
        return response.json()['result']
    except:
        if type(response) is int:
            return 'Timeout'
        else:
            resp = str(response.status_code) + ': ' + str(response.reason)
            return resp

# Description: gets up to 3 background colors and up to 3 foreground colors
# Input: takes the json response as input
# Output: returns a single array of non-duplicate colors
def process_json_response(json):
    unprocessed_background = json['colors']['background_colors']
    processed_background = []
    unprocessed_foreground = json['colors']['foreground_colors']
    processed_foreground = []

    for color in unprocessed_background:
        processed_background += [color['html_code']]

    for color in unprocessed_foreground:
        processed_foreground += [color['html_code']]

    return eliminate_duplicates(processed_background, processed_foreground)

# Description: eliminates duplicates from the two target arrays
# Input: takes the foreground and background color arrays as input
# Output: returns a single array with all colors from both that aren't duplicates
def eliminate_duplicates(background, foreground):
    to_return = foreground
    for color in background:
        if color not in to_return:
            to_return += [color]
    return to_return

# Description: gets the target color from the array of options
# Input: takes a single array of colors as input
# Output: returns a random entry from the array
def pick_color(color_options):
    length = len(color_options)
    index = random.randrange(0, length)
    return color_options[index]

# Description: gets a color scheme based on the target color
# Input: hex color code with hashtag
# Output: json response from API
def get_json_response_color_scheme(hex_color):
    #slicing the # off
    hex_color = hex_color[1:]
    response = requests.get(the_color_api_scheme_url + hex_color)
    return response.json()

# Description: picks the color from the API- not the lightest but also not nearly the darkes
# Input: unprocessed json response
# Output: lightest hex color code if hsl is greater than 75, if it is less than, it returns the 
# lighest color to be rerun (to get a lighter version of it)
def process_json_response_color_scheme(response):
    colors = response['colors']
    returnable_colors = {}
    
    returnable_colors['dark'] = colors[2]['hex']['value']

    for color in colors:
        hsl = color['hsl']['l']
        if hsl >= 75:
            returnable_colors['light'] = color['hex']['value']
            return returnable_colors

    returnable_colors['light'] = colors[-1]['hex']['value']
    returnable_colors['placeholder'] = ['not_finished']
    return returnable_colors
