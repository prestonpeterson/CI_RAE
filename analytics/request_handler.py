#!/usr/bin/env python
from analytics import bot_help
from analytics import karma_breakdown
from analytics import user_activity
from analytics import word_cloud
from analytics import word_count
from analytics import best_worst
import praw
import threading

class RequestThread(threading.Thread):
    def __init__(self, comment, reddit_client):
        threading.Thread.__init__(self)
        self.comment = comment
        self.reddit_client = reddit_client
    def run(self):
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
                reply = bot_help.ci_rae_help(self.comment)
            elif requests[1] == 'best_worst':
                reply = image_cloud.image_cloud(redditor_object)
            elif requests[1] == 'karma_breakdown':
                reply = karma_breakdown.karma_breakdown(redditor_object)
            elif requests[1] == 'user_activity':
                reply = user_activity.user_activity(redditor_object)
            elif requests[1] == 'word_cloud':
                reply = word_cloud.word_cloud(redditor_object)
            elif requests[1] == 'word_count':
                reply = word_count.word_count(redditor_object)
            else:
                reply = bot_help.ci_rae_help(self.comment)
            self.comment.reply(reply)
            print('Reply sent.')
        except:
            print('error, marking mention as read')
            self.comment.mark_as_read()


