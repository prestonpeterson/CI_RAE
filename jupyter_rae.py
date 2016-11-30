import matplotlib.pyplot as plt
import numpy as np
import operator
import praw
import os
from wordcloud import WordCloud, STOPWORDS
from ipywidgets import widgets
from IPython.html.widgets import *
from IPython.display import display
from operator import itemgetter
from analytics import word_cloud, karma_breakdown, user_interests, best_worst, frequent_words, location_interests, locations, profanity, sentiment_search, snarkiness, user_activity, word_count, bot_help
from bot.settings import user_agent
from IPython.display import clear_output

def set_limit(Limit):
    set_limit = Limit


def handle_submit(sender):
    display(best_worst_b)
    display(karma_breakdown_b)
    display(location_interests_b)
    display(snarkiness_b)
    display(user_activity_b)
    display(user_interests_b)
    display(word_cloud_b)
    display(word_count_b)


def clear_button_clicked(b):
    clear_output()


def on_button_clicked(b):
    reddit_u = reddit_client.get_redditor(text.value)

    if b == best_worst_b:
        print(best_worst.best_worst(reddit_u))
    elif b == karma_breakdown_b:
        karma_breakdown.karma_breakdown(reddit_u, debug=True)
    elif b == location_interests_b:
        print(location_interests.location_interests(reddit_u))
    elif b == snarkiness_b:
        print(snarkiness.snarkiness(reddit_u))
    elif b == user_activity_b:
        user_activity.user_activity(reddit_u, debug=True)
    elif b == user_interests_b:
        user_interests.interests(reddit_u, debug=True)
    elif b == word_cloud_b:
        word_cloud.word_cloud(reddit_u, debug=True)
    elif b == word_count_b:
        word_count.word_count(reddit_u, debug=True)
    else:
        bot_help.ci_rae_help(reddit_u)

if __name__ == '__main__':
    text = widgets.Text(description ="Redditor:")
    clear_b              = widgets.Button(description ="Clear Analytics")
    best_worst_b         = widgets.Button(description="Best Worst")
    karma_breakdown_b    = widgets.Button(description="Karma Breakdown")
    location_interests_b = widgets.Button(description="Location Interests")
    snarkiness_b         = widgets.Button(description="Snarkiness")
    user_activity_b      = widgets.Button(description="User Activity")
    user_interests_b     = widgets.Button(description="User Interests")
    word_cloud_b         = widgets.Button(description="Word Cloud")
    word_count_b         = widgets.Button(description="Word Count")
    interaction          = widgets.interact(description ="Return Limit")

    # frequent_words_b     = widgets.Button(description="Frequent Words") # Subreddit
    # user_agent = 'Reddit Analytics Engine, written by CSUCI students'
    reddit_client = praw.Reddit(user_agent=user_agent)

    set_limit = 100

    # Initialize callbacks (events)
    text.on_submit(handle_submit)
    best_worst_b.on_click(on_button_clicked)
    karma_breakdown_b.on_click(on_button_clicked)
    location_interests_b.on_click(on_button_clicked)
    snarkiness_b.on_click(on_button_clicked)
    user_activity_b.on_click(on_button_clicked)
    user_interests_b.on_click(on_button_clicked)
    word_cloud_b.on_click(on_button_clicked)
    word_count_b.on_click(on_button_clicked)
    clear_b.on_click(clear_button_clicked)

    # Display textbox and clear button
    display(text)
    display(clear_b)

    # interact(set_limit, Limit=(10,500,10), description="Return Limit")



