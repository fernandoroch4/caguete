import os
from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from os.path import join, dirname

class TwitterApi:
    def __init__(self):
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.key = os.getenv('T_KEY')
        self.secrect = os.getenv('T_SECRET')
        self.token = os.getenv('T_TOKEN')
        self.token_secret = os.getenv('T_TOKEN_SECRET')

    def connect(self):
        try:
            return TwitterAPI(self.key, self.secrect, self.token, self.token_secret)
        except OSError as err:
            return "OS error: {0}".format(err)
        except:
            return "Unexpected error:", sys.exc_info()[0]

    def post(self, textToPost):
        try:
            response = self.connect().request('statuses/update', {'status': textToPost})
            return 'SUCCESS' if response.status_code == 200 else 'PROBLEM: ' + response.text
        except OSError as err:
            return "OS error: {0}".format(err)
        except:
            return "Unexpected error:", sys.exc_info()[0]