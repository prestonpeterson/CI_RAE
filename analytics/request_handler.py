#!/usr/bin/env python

from bot.bot_client import response_queue
import threading

class RequestThread(threading.Thread):
    def __init__(self, comment):
        threading.Thread.__init__(self)
        self.comment = comment
    def run(self):
        requests = self.comment.body.lower().split(" ")
        print("requester = ", self.comment.author)
        for request in requests[1:]:
            print("request = ", request)
        response = ["Response: "]
        # perform the user requests
        # then reply to the user's comment
        response_queue.add((self.comment, response))

