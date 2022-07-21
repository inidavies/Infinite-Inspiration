import unittest
import requests
import sys

sys.path.append('../Infinite-Inspiration')
from color import background_color  # noqa E402

the_color_api_id_url = 'https://www.thecolorapi.com/id?hex='


class ImageUnitTests(unittest.TestCase):
    def setUp(self):
        self.bing_url = "https://th.bing.com/th/id/OIP."
        self.bing_url += "LIyeXFdvM83UkH_jNud3zwHaE5?pid=ImgDet&rs=1"
        self.unsplash_url = "https://source.unsplash.com/gySMaocSdqs/w=600"
        self.shortened_url = "https://tinyurl.com/2area6w6"

    def testIsDictionary(self):
        bing_data = background_color(self.bing_url)
        self.assertIsInstance(bing_data, dict)

    def testIsDictionaryUnsplash(self):
        unsplash_data = background_color(self.unsplash_url)
        self.assertIsInstance(unsplash_data, dict)

    def testIsDictionaryShortened(self):
        shortened_url_data = background_color(self.shortened_url)
        self.assertIsInstance(shortened_url_data, dict)

    def testLengthOfDictionary(self):
        unsplash_data = background_color(self.unsplash_url)
        bing_data = background_color(self.bing_url)
        self.assertIsInstance(unsplash_data, dict)
        self.assertIsInstance(bing_data, dict)
        self.assertEqual(len(unsplash_data), 2)
        self.assertEqual(len(bing_data), 2)

    def testLightColorResponseHSLLigtnessUnsplash(self):
        unsplash_data = background_color(self.unsplash_url)
        self.assertIsInstance(unsplash_data, dict)
        light = unsplash_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()
        response = response['hsl']['l']
        self.assertGreaterEqual(response, 75)

    def testLightColorResponseHSLLightnessBing(self):
        bing_data = background_color(self.bing_url)
        self.assertIsInstance(bing_data, dict)
        light = bing_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()
        response = response['hsl']['l']
        self.assertGreaterEqual(response, 75)

    def testLightColorResponseHSLLightnessShortened(self):
        shortened_url_data = background_color(self.shortened_url)
        self.assertIsInstance(shortened_url_data, dict)
        light = shortened_url_data['light'][1:]
        response = requests.get(the_color_api_id_url + light).json()
        response = response['hsl']['l']
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
