import unittest
import requests
import sys

sys.path.append('../Infinite-Inspiration')
from color import background_color

the_color_api_id_url = 'https://www.thecolorapi.com/id?hex='

class ImageUnitTests(unittest.TestCase):
    def setUp(self):
        self.unsplash_data = background_color("https://source.unsplash.com/gySMaocSdqs/w=600")
        self.bing_data = background_color("https://th.bing.com/th/id/OIP.LIyeXFdvM83UkH_jNud3zwHaE5?pid=ImgDet&rs=1")
        self.shortened_url_data = background_color("https://tinyurl.com/2area6w6")

    def testIsDictionary(self):
        self.assertIsInstance(self.bing_data, dict)

    def testIsDictionaryUnsplash(self):
        self.assertIsInstance(self.unsplash_data, dict)
    
    def testIsDictionaryShortened(self):
        self.assertIsInstance(self.shortened_url_data, dict)

    def testLengthOfDictionary(self):
        self.assertEqual(len(self.unsplash_data), 2)
        self.assertEqual(len(self.bing_data), 2)

    def testLightColorResponseHSLLigtnessUnsplash(self):
        light = self.unsplash_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()['hsl']['l']
        self.assertGreaterEqual(response, 75)

    def testLightColorResponseHSLLightnessBing(self):
        light = self.bing_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()['hsl']['l']
        self.assertGreaterEqual(response, 75)

    def testLightColorResponseHSLLightnessShortened(self):
        light = self.shortened_url_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()['hsl']['l']
        self.assertGreaterEqual(response, 75)
    
    def testNotUrlResponseIsInt(self):
        non_url = background_color("fklsajfl")
        self.assertIsInstance(non_url, int)
        self.assertEqual(non_url, -1)
    
    def testNonImageUrlResponseIsInt(self):
        non_image_url = background_color("https://google.com")
        self.assertIsInstance(non_image_url, int)
        self.assertEqual(non_image_url, -1)

if __name__ == '__main__':
    unittest.main()