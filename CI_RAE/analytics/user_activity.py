import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import math


class CIUserActivity:
    def __init__(self, r_user, time_zone='pst'):
        self.reddit_user = r_user
        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        self.thing_limit = 100
        #Dictionary that contains the indexes to access information in the datetime.tuple()
        self.datetime_ndx = {'year': 0, 'month': 1, 'day': 2, 'hour': 3,
                              'min': 4, 'sec': 5, 'wday': 6, 'yday': 7}

        self.time_zone = time_zone #TODO: Implement timezone

    def user_activity(self):
        generated = self.reddit_user.get_comments(limit=self.thing_limit)

        #The hour that the user has commented
        comment_times = { 0: 0,  1: 0,  2: 0, 3: 0, 4: 0, 5: 0,
                          6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0,
                          12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0,
                          18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0 }

        for r_comment in generated:
            # Apparently its UTC, but for some reason the format is in PST???
            print(datetime.fromtimestamp(r_comment.created_utc))
            dt = datetime.fromtimestamp(r_comment.created_utc).timetuple()
            hour_posted = dt[self.datetime_ndx['hour']]
            comment_times[hour_posted] += 1

        keys = np.array(list(comment_times.keys()))
        values = np.array(list(comment_times.values()))
        # Convert values to decimal percentage notation
        values = values / np.sum(values)

        # Generate the number of y-ticks the graph would need.
        # Ex. if the largest value only goes up to .23, max_y_tick would be 5 + 1 [0% 5% 10% 15% 20% 25%]
        max_y_tick = math.ceil(np.amax(values) * 20) + 1

        bar_width = 1
        fig, ax = plt.subplots()
        ax.bar(keys, values, bar_width, align='center')

        ax.set_title("Active Redditor Times: " + self.reddit_user.name)
        ax.set_xlabel("Time (PST)")
        ax.set_ylabel("Percentage of comments posted", rotation='vertical')
        ax.set_xlim([0,23])
        ax.axis('tight')

        ax.set_xticks(keys + bar_width)
        ax.set_yticks([x * .05 for x in range(max_y_tick)])

        ax.set_xticklabels(keys, rotation='vertical')
        ax.set_yticklabels(['{:3.0f}%'.format(x * 5) for x in range(max_y_tick)])
        #saves a png of the generated report
        plt.savefig("./generated_reports/"+self.user_name+"_wordcloud.png")
        plt.show()
