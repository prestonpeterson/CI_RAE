import re
<<<<<<< HEAD
from analytics.locations import US_States
from analytics.locations import countries
=======
from analytics.locations import *
>>>>>>> refs/remotes/origin/master

"""@package docstring
Allows the user to recieve a list of locations they have recently (up to 1000 items) mentioned.
Locations now only include countries and U.S. states which are grabbed from locations.py.
"""

found_locations = []
"""@var reply A formatted string used to reply back to user.
"""
def lookfor_locations(word):
    if word not in found_locations and (word in US_States or word in countries):
        found_locations.append(word)

def location_interests(reddit_user):
    """@param reddit_user A reddit user object
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
        reply += "+ [{0}](https://www.google.com/maps/place/{0})    ".format(location)
    return reply

if __name__ == '__main__':
    import praw
    #from bot.settings import user_agent
    client = praw.Reddit(user_agent="Reddit Analytics Engine, written by CSUCI students")
    reddit_u = client.get_redditor('giantmatt')
    answer = location_interests(reddit_u)
    print(answer)