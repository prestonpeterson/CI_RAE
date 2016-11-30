# \copyright GNU Public License.
# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford  
# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

"""@package docstring
Allows the user to recieve a list of locations they have recently (up to 1000 items) mentioned.
Locations now only include countries and U.S. states which are grabbed from locations.py.
"""

import re
from analytics.locations import *

found_locations = [] #used to keep track of locations already found

def lookfor_locations(word):
    """Checks to see if a location has already been looked at and checks if it exists in the lists
       @param word: Location to check
    """
    if word not in found_locations and (word in US_States or word in countries):
        found_locations.append(word)

def location_interests(reddit_user):
    """Checks the user's account history for references of certain locations
        @param reddit_user: A reddit user object to access data
        @return: The formated reply to the user
    """
    print("Checking for locations mentioned in user post titles...")
    submissions = reddit_user.get_submitted(limit=None)
    for submission in submissions:
        title = submission.title
        for word in title.split():
            word = re.sub(r'[^a-zA-Z\s]', '', word) #regex removes any special characters and digits
            lookfor_locations(word)

    print("Checking for locations mentioned in user post's body...")
    submissions = reddit_user.get_submitted(limit=None)
    for submission in submissions:
        body = submission.selftext
        for word in body.split():
            word = re.sub(r'[^a-zA-Z\s]', '', word) #regex removes any special characters and digits
            lookfor_locations(word)

    print("Checking for locations mentioned in user comments...")
    comments = reddit_user.get_comments(limit=None)
    for comment in comments:
        body = comment.body
        for word in body.split():
            word = re.sub(r'[^a-zA-Z\s]', '', word) #regex removes any special characters and digits
            lookfor_locations(word)

    reply = "## Based on your recent activity, here are some places you mentioned.\n\n***\n\n"
    for location in found_locations:
        reply += "+ [{0}](https://www.google.com/maps/place/{0})\n\n".format(location)
    return reply

if __name__ == '__main__':
    import praw
    #from bot.settings import user_agent
    client = praw.Reddit(user_agent="Reddit Analytics Engine, written by CSUCI students")
    reddit_u = client.get_redditor('giantmatt')
    answer = location_interests(reddit_u)
    print(answer)
