import unittest
import os
from dotenv import load_dotenv
from os.path import join, dirname
from TwitterAPI import TwitterAPI

class TestTwitterAPI(unittest.TestCase):
    def test_apiTwitter(self):
        dotenv_path = join(dirname(dirname(__file__)), '.env')
        load_dotenv(dotenv_path)

        api = TwitterAPI(os.getenv('T_KEY'),
                         os.getenv('T_SECRET'),
                         os.getenv('T_TOKEN'),
                         os.getenv('T_TOKEN_SECRET'))
        self.__api = api
        tweet = self.__api.request('statuses/home_timeline', {'count':1})
        self.assertIn('text', tweet.text)

if __name__ == '__main__':
    unittest.main()