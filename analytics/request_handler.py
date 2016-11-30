#!/usr/bin/env python

# \copyright GNU Public License.
# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford  
# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

import threading
from analytics import best_worst, bot_help, karma_breakdown, user_activity, \
    word_cloud, word_count, sentiment_search, location_interests, snarkiness, user_interests

class RequestThread(threading.Thread):
    """
    Threaded class that resolves user request parameters, calls appropriate analytic functions, and sends
    string result to user via a comment on Reddit.
    """
    def __init__(self, comment, reddit_client):
        """
        @ param comment Reddit comment object
        @param reddit_client Reddit client object
        """
        threading.Thread.__init__(self)
        self.comment = comment
        self.reddit_client = reddit_client
    def run(self):
        """
        Run the request thread
        """
        requests = self.comment.body.lower().split(" ")
        print("requester = ", self.comment.author)
        if len(requests) >= 2:
            print("command = ", requests[1])
        try:
            if len(requests) <= 2:
                redditor_object = self.reddit_client.get_redditor(self.comment.author)
            else:
                redditor_object = self.reddit_client.get_redditor(requests[2])
            if len(requests) <= 1:
                reply = bot_help.ci_rae_help(redditor_object)
            elif requests[1] == 'best_worst':
                reply = best_worst.best_worst(redditor_object)
            elif requests[1] == 'karma_breakdown':
                reply = karma_breakdown.karma_breakdown(redditor_object)
            elif requests[1] == 'user_activity':
                reply = user_activity.user_activity(redditor_object)
            elif requests[1] == 'word_cloud':
                reply = word_cloud.word_cloud(redditor_object)
            elif requests[1] == 'word_count':
                reply = word_count.word_count(redditor_object)
            elif requests[1] == 'snarkiness':
                reply = snarkiness.snarkiness(redditor_object)
            elif requests[1] == 'locations':
                reply = location_interests.location_interests(redditor_object)
            elif requests[1] == 'sentiment_search' and len(requests) >= 3:
                term = ' '.join(requests[2:])
                print('search term = ', term)
                reply = sentiment_search.sentiment_search(self.reddit_client, term)
            elif requests[1] == 'user_interests':
                reply = user_interests.interests(redditor_object)
            else:
                reply = bot_help.ci_rae_help(self.comment)
            print(reply)
            self.comment.reply(reply)
            print('Reply sent.')
        except Exception as e:
            print("Exception: ", e)


