import praw
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np

class CIRaeUserActivity:
    def __init__(self, r_user, time_zone):
        self.reddit_user = r_user
        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        self.thing_limit = 100
        self.hourNdx = 3
        self.time_zone = time_zone

    def user_activity(self):
        generated = self.reddit_user.get_comments(limit=self.thing_limit)

        comment_times = { 0: 0,  1: 0,  2: 0, 3: 0, 4: 0, 5: 0,
                          6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0,
                          12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0,
                          18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0 }

        for r_comment in generated:
            print(datetime.fromtimestamp(r_comment.created_utc))
            dt = datetime.fromtimestamp(r_comment.created_utc).timetuple()
            hour_posted = dt[self.hourNdx]
            comment_times[hour_posted] += 1

        keys = np.array(list(comment_times.keys()))
        values = np.array(list(comment_times.values()))
        values = values / np.sum(values)
        width = 1
        fig, ax = plt.subplots()
        ax.bar(keys, values, width, align='center')
        #ax.axis('tight')
        ax.set_title("Active redditor time: " + self.reddit_user.name)
        ax.set_xlabel("Time")
        ax.set_ylabel("Percentage of comments posted", rotation='vertical')
        ax.set_xticks(keys + width)
        ax.set_xticklabels(keys, rotation='vertical')
        #ax.tight_layout()
        #saves a png of the generated report
        # plt.savefig(user_name+'_karma_breakdown.png')
        plt.show()
