import random, requests
#TODO: Go here (https://imagga.com/profile/dashboard) to get your API key and secret to run locally
#https://www.thecolorapi.com/docs to get brightness (to pick suitable color)

imagga_api_key = ""
imagga_api_secret = ""
imagga_color_url = "https://api.imagga.com/v2/colors?image_url="

#Description: handles the api call to imagga
#Input: takes the image url as input
#Output: returns the response in json format
def get_json_response_imagga(img_url):
    response = requests.get(imagga_color_url + img_url, auth=(imagga_api_key, imagga_api_secret))
    return response.json()

#Description: eliminates duplicates from the two target arrays
#Input: takes the foreground and background color arrays as input
#Output: returns a single array with all colors from both that aren't duplicates
def eliminate_duplicates(background, foreground):
    to_return = foreground
    for color in background:
        if color not in to_return:
            to_return += [color]
    return to_return

#Description: gets up to 3 background colors and up to 3 foreground colors
#Input: takes the json response as input
#Output: returns a single array of non-duplicate colors
def process_json_response(json):
    unprocessed_background = json['result']['colors']['background_colors']
    processed_background = []
    unprocessed_foreground = json['result']['colors']['foreground_colors']
    processed_foreground = []

    for color in unprocessed_background:
        processed_background += [color['html_code']]
    
    for color in unprocessed_foreground:
        processed_foreground += [color['html_code']]
    
    return eliminate_duplicates(processed_background, processed_foreground)

#Description: gets the target color
#Input: takes a single array of colors as input
#Output: returns a random entry from the array
def pick_color(color_options):
    length = len(color_options)
    index = random.randrange(0, length)
    return color_options[index]

#Description: gets a color scheme based on the target color
#Input: hex color code with hashtag
#Output: json response from API
def get_json_response_color_scheme(hex_color):
    hex_color = hex_color[1:]
    response = requests.get('https://www.thecolorapi.com/scheme?hex='+hex_color)
    return response.json()

#Description: picks the color from the API- not the lightest but also not nearly the darkes
#Input: unprocessed json response
#Output: hex color code
def process_json_response_color_scheme(response):
    colors = response['colors']
    target = colors[-2]
    return target['hex']['clean']

#USE THIS TO CALL IN OTHER LOCATIONS
def get_background_color(img_url):
    response = get_json_response_imagga(img_url)
    processed_response = process_json_response(response)
    color = pick_color(processed_response)
    color_scheme = get_json_response_color_scheme(color)
    final_color = process_json_response_color_scheme(color_scheme)
    return final_color

print(get_background_color("https://th.bing.com/th/id/OIP.LIyeXFdvM83UkH_jNud3zwHaE5?pid=ImgDet&rs=1"))
