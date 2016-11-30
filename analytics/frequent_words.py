# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

"""@package docstring
Provides a function that scans a subreddit's submissions and records frequency of word use.
Following, a report is generated and uploaded to imgur.com.
"""

from wordcloud import STOPWORDS
from operator import itemgetter
from imgur import upload
import matplotlib.pyplot as plt
import numpy as np
import os
import re
import difflib

# Syntax:
# subreddit_get['hot']['none']
# subreddit_get['top']['today'] etc.
subreddit_get = {
            'hot': {'none': 'get_hot'},
            'rising': {'none': 'get_rising'},
            'new': {'none': 'get_new'},
            'controversial': {
                  'none': 'get_controversial',
                   'all': 'get_controversial_from_all',
                 'today': 'get_controversial_from_day',
             'past_hour': 'get_controversial_from_hour',
            'past_month': 'get_controversial_from_month',
             'past_week': 'get_controversial_from_week',
             'past_year': 'get_controversial_from_year'},

            'top': {
                  'none': 'get_top',
                   'all': 'get_top_from_all',
                 'today': 'get_top_from_day',
             'past_hour': 'get_top_from_hour',
            'past_month': 'get_top_from_month',
             'past_week': 'get_top_from_week',
             'past_year': 'get_top_from_year'}
            }

def frequent_words(subreddit, category='hot', time='none', save_path='', submission_limit=5, debug=False, skip_more_comments=True):
    """
    Collects submissions from a given subreddit, and produces word counts. These counts are
    used to produce a graph that is uploaded to imgur.com. The URI for this image is then
    returned as a python string to the calling function.

    :param subreddit:          Instance of Subreddit object from praw.objects
    :param category:           String identifier for category
    :param time:               Time used for fetching
    :param save_path:          Location to store temporary image file
    :param submission_limit:   Limit to number of submissions used to generate report
    :param debug:              Boolean controlling debug output
    :param skip_more_comments: Boolean to signal skipping of additional comments
    :return:                   String containing URI for page on imgur.com with image.
    """

    # A dictionary containing all the words in the comments
    # Key (String): the word used
    # Value (int): count of how many times the word was said
    counted_comments = {}
    # using stopwords from wordcloud to remove insignificant words ('The', 'at', etc.)
    stop_words = set(STOPWORDS)
    regex_pattern = r"([a-zA-Z']+)"
    stop_words.add('i')
    stop_words.add('*')
    stop_words.add('-')

    # Get submissions from subreddit
    get = getattr(subreddit, subreddit_get[category][time])
    all_submissions = get(limit=submission_limit)

    for submission in all_submissions:
        # A list containing all the words in the comment
        words_in_comment = []

        # We also take into consideration the submission's text as well
        submission_text = ''.join([submission.title, ' ', submission.selftext])
        lines = submission_text.split()
        for x in range(len(lines)):
            words_in_comment.append(lines[x])
        # Populate words_in_comment from reddit submission
        for comment in submission.comments:
            if isinstance(comment, praw.objects.Comment):
                lines = comment.body.split()
                for x in range(len(lines)):
                    # Regex pattern that of words only
                    word = re.search(regex_pattern, lines[x])
                    if word is not None:
                        word = str.lower(word.group(0))
                        if word not in stop_words:
                            match = difflib.get_close_matches(word, list(counted_comments.keys()))
                            if not match:
                                counted_comments[word] = 1
                            else:
                                counted_comments[match[0]] += 1
            else:
                if skip_more_comments:
                    continue
                # TODO: Implement submission.replace_more_comments, but this requires that you adhere to the Reddit API guidelines

    # Sorts the dictionary by value, then reverses
    sorted_x = sorted(counted_comments.items(), key=itemgetter(1), reverse=True)
    top20 = sorted_x[:20]

    # Seperate keys and values
    sorted_keys = list(map(itemgetter(0), top20))

    sorted_values = list(map(itemgetter(1), top20))

    max_y_tick = np.amax(sorted_values) + 1
    bar_width = 1
    sorted_range = np.array(range(len(sorted_keys)))

    fig, ax = plt.subplots()
    ax.bar(sorted_range, sorted_values, bar_width, align='center')

    ax.set_title("Top 20 most common words in /r/" + subreddit.display_name + ' category: ' + category)

    ax.set_xlabel("Word")
    ax.set_ylabel("Frequency", rotation='vertical')

    ax.set_xlim([0, len(sorted_range)])
    ax.set_ylim([0, max_y_tick])

    fig.tight_layout()  # This is apparently supposed to give room to the x labels
    ax.axis('tight')

    ax.set_xticks(sorted_range)

    ax.set_xticklabels(sorted_keys, rotation='vertical')

    # Adds space to the bottom so that the xticklabels can be displayed
    # f(x) = (x * 2 + 4) / 100
    # x = the length of the biggest word | Ex. len('hello') = 5
    longest_key = len(max(sorted_keys, key=len))
    bottom_padding = float(longest_key * 2 + 4) / 100
    plt.subplots_adjust(bottom=bottom_padding)

    # Saves a png of the generated report
    file_name = os.path.join(save_path + 'r-' + subreddit.display_name + '_word_count.png')
    plt.savefig(file_name)

    # Remove local copy of png
    if not debug:
        image_link = upload.upload_image(file_name)
        os.remove(file_name)
        return image_link
    else:
        plt.show()
        # os.remove(file_name)
        return file_name


if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    reddit = praw.Reddit(user_agent)
    reddit.login(username='ci_rae', password='herpderp')
    subreddit = reddit.get_subreddit('pokemongo')  # pokemongo, LUL (Try it on The_Donald if you want some epik maymays)
    # Refer to the dictionary to see which category and time choices you can make
    frequent_words(subreddit, category='top', time='today', debug=True)
