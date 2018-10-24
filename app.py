#!/usr/bin/python3
#
# Coyright Caguete Bot
#
import sys
from module.twitter import TwitterApi
from source.deputadosRS import DeputadosRS

def main():
    deputadoRS = DeputadosRS()
    posts = deputadoRS.getTextToPost()
    if (posts):
        tweet = TwitterApi()
        for text in posts:
            tweet.post(text)
    else:
        sys.exit()

if __name__ == '__main__':
    main()