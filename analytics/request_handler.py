#!/usr/bin/env python
from analytics.bot_help import CIHelp
from analytics.image_cloud import CIImageCloud
from analytics.karma_breakdown import CIKarmaBreakdown
from analytics.user_activity import CIUserActivity
from analytics.word_cloud import CIWordCloud
from analytics.word_count import CIWordCount
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
            bh = CIHelp(self.comment)
            bh.help()
        elif requests[1] == 'image_cloud':
             ic = CIImageCloud(requests[2])
             ic.image_cloud()
        elif requests[1] == 'karma_breakdown':
            kb = CIKarmaBreakdown(requests[2])
            kb.word_cloud()
        elif requests[1] == 'user_activity':
            ua = CIUserActivity(requests[2])
            ua.user_activity()
        elif requests[1] == 'word_cloud':
            wc = CIWordCloud(requests[2])
            wc.word_cloud()
        elif requests[1] == 'word_count':
            wc = CIWordCount(requests[2])
            wc.word_count()
        else:
            self.comment.reply("Incorrect Format, please use /u/ci_rae <command> <target>")
            bh = CIHelp(self.comment)
            bh.help()
        response = ["Response: "]
        # perform the user requests
        # then reply to the user's comment
        #response_queue.add((self.comment, response))

