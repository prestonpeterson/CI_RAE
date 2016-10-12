#!/usr/bin/env python

import praw
from prawoauth2 import PrawOAuth2Mini
import time

from tokens import app_key, app_secret, access_token, refresh_token
from settings import scopes, user_agent

reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key,
                              app_secret=app_secret, access_token=access_token,
                              scopes=scopes, refresh_token=refresh_token)

def run_bot():
    oauth_helper.refresh()
    for comment in reddit_client.get_comments('test'):
        if comment.body.lower().startswith('ci_rae '):
            print('Found request')
            comment.reply('Hello!')

while True:
    try:
        run_bot()
    except praw.errors.OAuthInvalidToken:
        # access tokens expire hourly, so must be periodically refreshed
        oauth_helper.refresh()
    except praw.errors.RateLimitExceeded as rle:
        # Reddit limits number of comments you can make per minute
        # depending on factors like age of your account and karma score
        # If bot tries to comment too frequently, this exception will be caught
        print(rle.error_type, rle.message)
        print("Sleeping for ", rle.sleep_time, " seconds")
        time.sleep(rle.sleep_time)

