#!/usr/bin/env python

import praw
from bot.prawoauth2 import PrawOAuth2Mini
import time
from bot.tokens import app_key, app_secret, access_token, refresh_token
from bot.settings import scopes, user_agent, user_name, user_pass
from analytics.request_handler import RequestThread



class BotClient:
    def __init__(self):
        print("Starting up the reddit bot...")
        print("Authenticating to Reddit...")
        self.reddit_client = praw.Reddit(user_agent=user_agent)
        self.oauth_helper = PrawOAuth2Mini(self.reddit_client, app_key=app_key,
                                      app_secret=app_secret, access_token=access_token,
                                      scopes=scopes, refresh_token=refresh_token)
        self.reddit_client.login(user_name, user_pass, disable_warning=True)
        print("Authentication successful!")

        self.cache = set() # comment ids can/should be removed from this set once they have been replied to
        self.subreddit_wait_times = {} # rate limit wait times for subreddits
        self.current_sub = ''
        print("Initiating the Listening process")

        # infinite loop to run the listener in
        while True:
            try:
                self.listen_for_mentions()
            except praw.errors.OAuthInvalidToken:
                # access tokens expire hourly, so must be periodically refreshed
                self.oauth_helper.refresh()
            except praw.errors.RateLimitExceeded as rle:
                # Reddit limits number of comments you can make per minute
                # depending on factors like age and karma score of the bot's reddit account
                # If bot tries to comment too frequently, this exception will be caught
                print(rle.error_type, rle.message)
                print("Sleeping for ", rle.sleep_time, " seconds")
                self.add_subreddit_wait_time(rle.sleep_time, self.current_sub, self.subreddit_wait_times)
                time.sleep(rle.sleep_time)
            except Exception as e:
                print('Error: ', e)

    def check_sub_wait(self, subreddit, subs):
        """
        checks if the given subreddit is in the dictionary of subs that the bot is timed out from
        :param subreddit: subreddit to check for existence in the dictionary
        :param subs: the list of subs that the bot is currently timed out from
        :return: True if the bot is currently timed out from the given subreddit. False otherwise
        """
        s = subreddit.display_name
        if s in subs:
            now = time.time()
            wait_time = subs[s]
            if now >= wait_time:
                # bot is no longer timed out from given subreddit. remove this subreddit from the subs dictionary
                del subs[s]
            else:
                # bot is currently timed out from the given subreddit
                return True
        return False

    def add_subreddit_wait_time(self, subreddit_timeout, subreddit, subs):
        """
        Add current subreddit timeout to subreddit_wait_times list.
        :param subreddit_timeout: number of seconds til bot can post to this subreddit
        :param subreddit: the subreddit that the bot is currently timed out from
        :param subs: the list of subreddits that the bot is timed out from
        """
        now = time.time()
        s = subreddit.display_name
        subs[s] = now + subreddit_timeout

    def listen_for_mentions(self):
        """
        Refresh reddit authentication token, check for new Reddit Mentions of /u/ci_rae.
        If new mentions are found, mark them as read hand them over to the request handler class.
        """
        self.oauth_helper.refresh()
        mentions = self.reddit_client.get_mentions()

        # Check new mentions
        for m in mentions:
            self.current_sub = m.subreddit

            if m.id in self.cache:
                continue
            if m.subject != 'username mention':
                m.mark_as_read()
                continue

            if self.check_sub_wait(m.subreddit, self.subreddit_wait_times):
                continue

            for reply in m.replies:
                if reply.author.name == 'ci_rae':
                    self.cache.add(m.id)

            # Process the message
            if m.id not in self.cache:
                print("Found request")
                thread = RequestThread(m, self.reddit_client)
                thread.start()
                m.mark_as_read()

            self.cache.add(m.id)

        time.sleep(2)


if __name__ == "__main__":
    BotClient()


