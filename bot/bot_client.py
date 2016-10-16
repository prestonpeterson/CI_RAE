#!/usr/bin/env python

import praw
from bot.prawoauth2 import PrawOAuth2Mini
import time
from bot.tokens import app_key, app_secret, access_token, refresh_token
from bot.settings import scopes, user_agent, subreddits, SLEEP_TIME, user_name, user_pass
from analytics import request_handler

cache = set() # comment ids can/should be removed from this set once they have been replied to
sub_wait = {} # rate limit wait times for subreddits
current_sub = ''

reddit_client = praw.Reddit(user_agent=user_agent)
oauth_helper = PrawOAuth2Mini(reddit_client, app_key=app_key,
                              app_secret=app_secret, access_token=access_token,
                              scopes=scopes, refresh_token=refresh_token)
reddit_client.login(user_name, user_pass, disable_warning=True)



def check_sub_wait(subreddit, subs):
    s = subreddit.display_name
    if s in subs:
        now = time.time()
        wait_time = subs[s]
        print('%i < %i?' % (now, wait_time))
        if now >= wait_time:
            del subs[s]
        else:
            return True
    return False

def add_sub_wait(sleep_time, subreddit, subs):
    now = time.time()
    s = subreddit.display_name
    subs[s] = now+sleep_time


def run_bot():
    oauth_helper.refresh()
    mentions = reddit_client.get_mentions()

    # Check new mentions
    for m in mentions:
        current_sub = m.subreddit

        if m.id in cache:
            continue
        if m.subject != 'username mention':
            m.mark_as_read()
            continue

        if check_sub_wait(m.subreddit, sub_wait):
            continue



        for reply in m.replies:
            if reply.author.name == 'ci_rae':
                cache.add(m.id)

        # Process the message
        if m.id not in cache:
            # Call Phillip's Request Handler class to process the user's request(s)
            print("Found request")
            m.reply("yao yao")
            m.mark_as_read()

        cache.add(m.id)

    time.sleep(SLEEP_TIME)

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
        add_sub_wait(rle.sleep_time.sleep_time, current_sub, sub_wait)
        time.sleep(rle.sleep_time)
    except Exception as e:
        print('Error: ', e)




