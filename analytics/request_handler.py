#!/usr/bin/env python
from analytics import image_cloud
from analytics import bot_help
from analytics import karma_breakdown
from analytics import user_activity
from analytics import word_cloud
from analytics import word_count
from analytics import best_worst
import praw
import threading

class RequestThread(threading.Thread):
    def __init__(self, comment):
        threading.Thread.__init__(self)
        self.comment = comment
    def run(self):

        user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

        r = praw.Reddit(user_agent=user_agent)

        requests = self.comment.body.lower().split(" ")
        print("requester = ", self.comment.author)
        print("command = ", requests[1])

        if requests[1] == 'help':
            bot_help(self.comment)
        elif requests[1] == 'best_worst':
            best_worst(self.comment, requests[2])
        elif requests[1] == 'image_cloud':
            image_cloud(requests[2], '')
        elif requests[1] == 'karma_breakdown':
            karma_breakdown(requests[2],'')
        elif requests[1] == 'user_activity':
            user_activity(requests[2])
        elif requests[1] == 'word_cloud':
            word_cloud(requests[2])
        elif requests[1] == 'word_count':
            word_count(requests[2])
        else:
            self.comment.reply("Incorrect Format, please use /u/ci_rae <command> <target>")
            bot_help(self.comment)
        response = ["Response: "]
        # perform the user requests
        # then reply to the user's comment
        #response_queue.add((self.comment, response))

