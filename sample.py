#!/usr/bin/python3
# Coyright Caguete Bot
import os
import time
import datetime
from TwitterAPI import TwitterAPI
from dotenv import load_dotenv
from os.path import join, dirname

# Loading environments variables
# Create .env file path
dotenv_path = join(dirname(__file__), '.env')
# Load file from path
load_dotenv(dotenv_path)

# Run every 12h (43200 seconds)
# It's necessary when we don't have a cron
every = 43200

# Define main function
def main():

    # Call api and send data to post
    print(twitter(get_data()))

# Twitter function
def twitter(post):
    api = TwitterAPI(os.getenv('T_KEY'),
                     os.getenv('T_SECRET'),
                     os.getenv('T_TOKEN'),
                     os.getenv('T_TOKEN_SECRET'))
    r = api.request('statuses/update', {'status': post})
    return 'SUCCESS' if r.status_code == 200 else 'PROBLEM: ' + r.text

# Get data from web
def get_data():
    post = datetime.datetime.now()
    return post

if __name__ == '__main__':
    while True:
        time.sleep(every)
        main()
