import praw
import matplotlib.pyplot as plt
import numpy as np
import operator
from operator import itemgetter
from datetime import datetime

class CIUserActivity:
    def __init__(self,user_name):
        self.user_name = user_name
        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        self.thing_limit = 100
        self.hourNdx = 3

    def user_activity(self):
        # Per the reddit API, user agent should follow format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
        user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

        r = praw.Reddit(user_agent=user_agent)


        #user_name = "ci_rae" #input("Please Enter a user to get their most active time of day by hour\n")

        user = r.get_redditor(self.user_name)

        generated = user.get_comments(limit=self.thing_limit)

        comment_times = { 0: 0,  1: 0,  2: 0, 3: 0,   4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0, 18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0, 24: 0 }

        for r_comment in generated:
            print(datetime.fromtimestamp(r_comment.created_utc))
            dt = datetime.fromtimestamp(r_comment.created_utc)
            hour_posted = dt.timetuple()[self.hourNdx]
            comment_times[hour_posted] += 1

        keys = list(comment_times.keys())
        values = list(comment_times.values())
        fig = plt.figure()
        plt.bar(range(len(values)), values, align='center')
        plt.title("Active redditor time: " + self.user_name.name)
        plt.xlabel("Time")
        plt.ylabel("Comment posted", rotation='vertical')
        plt.xticks(range(len(keys)), keys, rotation='vertical')
        plt.tight_layout()
        #saves a png of the generated report
        # plt.savefig(user_name+'_karma_breakdown.png')
        plt.show()
