import unittest
from module.twitter import TwitterApi

class TestTwitterAPI(unittest.TestCase):
    def test_apiTwitter(self):
        tweet = TwitterApi()
        connect = tweet.connect()
        timeline = connect.request('statuses/home_timeline', {'count':1})
        self.assertIn('text', timeline.text)

if __name__ == '__main__':
    unittest.main()