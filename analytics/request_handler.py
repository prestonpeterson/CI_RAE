#!/usr/bin/env python

import threading

class RequestThread(threading.Thread):
    def __init__(self, comment):
        threading.Thread.__init__(self)
        self.comment = comment
    def run(self):
        requests = self.comment.body.lower().split(" ")
        print("requester = ", self.comment.author)
        for request in requests:
            print("request = ", request)

