"""@package docstring
Provides a function to generate a graph of user activity on reddit, and then upload an image
of the report to imgur.com, and finally, return a string URI to the page on imgur.com.
"""

import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np
import math
import os
from imgur import upload


def user_activity(reddit_user, save_path='', debug=False):  # TODO: Implement timezone
    """
    :param reddit_user: Instance of Redditor object from praw.objects
    :param save_path:   Path to location for temporary saving of generated image
    :param debug:       Boolean to signal debugging output
    :return:            String containing URI link to generated image
    """

    # Set to grab a certain number of things from reddit...reddit wont return more than 1000
    thing_limit = 100
    # Dictionary that contains the indexes to access information in the datetime.tuple()
    datetime_ndx = {'year': 0, 'month': 1, 'day': 2, 'hour': 3,
                    'min': 4, 'sec': 5, 'wday': 6, 'yday': 7}
    generated = reddit_user.get_comments(limit=thing_limit)

    # The hour that the user has commented
    comment_times = { 0: 0,  1: 0,  2: 0, 3: 0, 4: 0, 5: 0,
                      6: 0, 7: 0, 8: 0, 9: 0, 10: 0, 11: 0,
                      12: 0, 13: 0, 14: 0, 15: 0, 16: 0, 17: 0,
                      18: 0, 19: 0, 20: 0, 21: 0, 22: 0, 23: 0 }

    for r_comment in generated:
        # Apparently its UTC, but for some reason the format is in PST???
        # print(datetime.fromtimestamp(r_comment.created_utc))
        dt = datetime.fromtimestamp(r_comment.created_utc).timetuple()
        hour_posted = dt[datetime_ndx['hour']]
        comment_times[hour_posted] += 1

    keys = np.array(list(comment_times.keys()))
    values = np.array(list(comment_times.values()))
    # Convert values to decimal percentage notation
    values = values / np.sum(values)

    # Generate the number of y-ticks the graph would need.
    # Ex. if the largest value only goes up to .23, max_y_tick would be 5 + 1 [0% 5% 10% 15% 20% 25%]
    max_y_tick = math.ceil(np.amax(values) * 20) + 1

    sorted_range = np.array(range(len(keys)))
    bar_width = 1
    fig, ax = plt.subplots()
    ax.bar(sorted_range, values, bar_width, align='center')

    ax.set_title("Active Redditor Times: " + str(reddit_user.name))

    ax.set_xlabel("Time (PST)")
    ax.set_ylabel("Percentage of comments posted", rotation='vertical')

    ax.set_xlim([0, 23])

    ax.set_xticks(sorted_range)
    ax.set_yticks([x * .05 for x in range(max_y_tick)])

    ax.set_xticklabels(keys, rotation='vertical')
    ax.set_yticklabels(['{:3.0f}%'.format(x * 5) for x in range(max_y_tick)])

    fig.tight_layout() # This is apparently supposed to give room to the x labels
    ax.axis('tight')

    # Saves a png of the generated report
    file_name = os.path.join(save_path + str(reddit_user.name) + '_user_activity.png')
    plt.savefig(file_name)

    # Remove local copy of png
    if not debug:
        image_link = upload.upload_image(file_name)
        os.remove(file_name)
        return image_link
    else:
        plt.show()
        os.remove(file_name)
        return file_name

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    user_activity(reddit_u, debug=True)
