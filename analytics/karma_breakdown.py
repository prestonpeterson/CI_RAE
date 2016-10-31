import matplotlib.pyplot as plt
import numpy as np
import operator
from operator import itemgetter
from imgur import upload

# TODO: Y Tick labels get squished together if a user's karma is high, implement scaling tick numbers
def karma_breakdown(reddit_user, save_path=''):
    # Set to grab a certain number of things from reddit...reddit wont return more than 1000
    thing_limit = 100

    generated = reddit_user.get_submitted(limit=thing_limit)

    karma_by_subreddit = {}

    for thing in generated:
        subreddit = thing.subreddit.display_name
        karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) + thing.score)

    # remove entries that have a value of 0
    removed_zeroes = {x:y for x, y in karma_by_subreddit.items() if y != 0}

    #sorts the dictionary by value, then reverses
    sorted_x = sorted(removed_zeroes.items(), key=operator.itemgetter(1), reverse=True)

    #get just the keys into a sorted list, and trim to get the top 20
    sorted_keys = list(map(itemgetter(0), sorted_x))
    del sorted_keys[20:]

    #get just the keys into a sorted values, and trim to get the top 20
    sorted_values = list(map(itemgetter(1), sorted_x))
    del sorted_values[20:]

    max_y_tick = np.amax(sorted_values) + 1
    bar_width = 1
    sorted_range = np.array(range(len(sorted_keys)))

    fig, ax = plt.subplots()
    ax.bar(sorted_range, sorted_values, bar_width, align='center')

    ax.set_title("Karma Breakdown of top 20 subreddits from User: " + reddit_user.name)

    ax.set_xlabel("Subreddit Name")
    ax.set_ylabel("Karma", rotation='vertical')

    ax.set_xlim([0, len(sorted_range)])
    ax.set_ylim([0, max_y_tick])

    fig.tight_layout() # This is apparently supposed to give room to the x labels
    ax.axis('tight')

    ax.set_xticks(sorted_range)
    ax.set_yticks(range(max_y_tick))

    ax.set_xticklabels(sorted_keys, rotation='vertical')

    # Saves a png of the generated report
    file_name = save_path + reddit_user.name + '_karma_breakdown.png'
    plt.savefig(file_name)
    image_link = upload.upload_image(file_name)
    return image_link
