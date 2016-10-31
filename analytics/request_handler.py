#!/usr/bin/env python
from analytics import image_cloud
from analytics import bot_help
from analytics import karma_breakdown
from analytics import user_activity
from analytics import word_cloud
from analytics import word_count
from analytics import best_worst
import threading

class RequestThread(threading.Thread):
    def __init__(self, comment, reddit_client):
        threading.Thread.__init__(self)
        self.comment = comment
        self.reddit_client = reddit_client
        print('request thread opened')
    def run(self):
        requests = self.comment.body.lower().split(" ")
        print("requester = ", self.comment.author)
        print("command = ", requests[1])
        if requests[1] == 'best_worst':
            reply = best_worst.best_worst(self.comment, self.reddit_client.get_redditor(requests[2]))
        elif requests[1] == 'image_cloud':
            reply = image_cloud.image_cloud(self.reddit_client.get_redditor(requests[2]))
        elif requests[1] == 'karma_breakdown':
            reply = karma_breakdown.karma_breakdown(self.reddit_client.get_redditor(requests[2]))
        elif requests[1] == 'user_activity':
            reply = user_activity.user_activity(self.reddit_client.get_redditor(requests[2]))
        elif requests[1] == 'word_cloud':
            reply = word_cloud.word_cloud(self.reddit_client.get_redditor(requests[2]))
        elif requests[1] == 'word_count':
            reply = word_count.word_count(self.reddit_client.get_redditor(requests[2]))
        else:
            reply = bot_help.ci_rae_help(self.comment)
        self.comment.reply(reply)
        print('Reply sent.')

