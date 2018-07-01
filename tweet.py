import os
from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from os.path import join, dirname

# Create .env file path.
dotenv_path = join(dirname(__file__), '.env')
# Load file from the path.
load_dotenv(dotenv_path)

TWEET_TEXT = "[Testing API] This is so exciting #2"

api = TwitterAPI(os.getenv('KEY'),
                 os.getenv('SECRET'),
                 os.getenv('TOKEN'),
                 os.getenv('TOKEN_SECRET'))

r = api.request('statuses/update', {'status': TWEET_TEXT})
print('SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text)
