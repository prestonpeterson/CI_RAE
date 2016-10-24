import praw
import matplotlib.pyplot as plt
import numpy as np
import operator
from operator import itemgetter


def karma_breakdown(reddit_user, save_path=''):
    #set to grab a certain number of things from reddit...reddit wont return more than 1000
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


    fig = plt.figure()
    plt.bar(range(len(sorted_values)), sorted_values, align='center')
    plt.title("Karma Breakdown of top 20 subreddits from User: " + reddit_user.name)
    plt.xlabel("Subreddit Name")
    plt.ylabel("Karma", rotation='vertical')
    plt.xticks(range(len(sorted_keys)), sorted_keys, rotation='vertical')
    plt.tight_layout()

    # Saves a png of the generated report
    file_name = save_path + reddit_user.name + '_karma_breakdown.png'
    plt.savefig(file_name)
    return file_name
