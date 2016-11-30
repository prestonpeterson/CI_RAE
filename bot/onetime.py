"""@package docstring
Uses OAuth to generate access tokens for bot account
"""

#!/usr/bin/env python

# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.
# import os

import praw
from bot.prawoauth2 import PrawOAuth2Server

from bot.tokens import app_key, app_secret
from bot.settings import user_agent, scopes

reddit_client = praw.Reddit(user_agent=user_agent)
oauthserver = PrawOAuth2Server(reddit_client, app_key=app_key,
                               app_secret=app_secret, state=user_agent,
                               scopes=scopes)

# start the server, this will open default web browser
# asking you to authenticate
oauthserver.start()
tokens = oauthserver.get_access_codes()
print(tokens)
