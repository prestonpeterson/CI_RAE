import praw
import matplotlib.pyplot as plt
import numpy as np
import operator
from operator import itemgetter


class CIKarmaBreakdown:
    def __init__(self,user_name):
        self.user_name = user_name
    def karma_breakdown(self):

        # Per the reddit API, user agent should follow format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
        user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

        r = praw.Reddit(user_agent=user_agent)

        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        thing_limit = 100
        # user_name = input("Please Enter a user to get their karma breakdown by subreddit:\n")

        user = r.get_redditor(self.user_name)

        generated = user.get_submitted(limit=thing_limit)

        karma_by_subreddit = {}

        for thing in generated:
            subreddit = thing.subreddit.display_name
            karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

        # remove entries that have a value of 0
        removed_zeroes = {x:y for x,y in karma_by_subreddit.items() if y!=0}

        #sorts the dictionary by value, then reverses
        sorted_x = sorted(removed_zeroes.items(), key=operator.itemgetter(1), reverse=True)

        #get just the keys into a sorted list, and trim to get the top 20
        sorted_keys = list(map(itemgetter(0), sorted_x))
        del sorted_keys[20:]

        #get just the keys into a sorted values, and trim to get the top 20
        sorted_values = list(map(itemgetter(1), sorted_x))
        del sorted_values[20:]

        fig = plt.figure()
        plt.bar(range(len(sorted_values)), sorted_values, align='center')
        #plt.title("Karma Breakdown of top 20 subreddits from User: " + self.user_name)
        plt.xlabel("Subreddit Name")
        plt.ylabel("Karma", rotation='vertical')
        plt.xticks(range(len(sorted_keys)), sorted_keys, rotation='vertical')
        plt.tight_layout()

        #saves a png of the generated report
        # plt.savefig(self.user_name+'_karma_breakdown.png')
        plt.show()
