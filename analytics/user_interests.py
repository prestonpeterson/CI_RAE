# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

"""@package docstring
This command generates a pie graph of a user's top interests by analyzing a user's most visited subreddits.
"""

from imgur import upload
from collections import OrderedDict
from pylab import *
import os


def interests(reddit_user, save_path='', debug=False):
    """Grabs a limited number of comments made by a user and determines the top subreddits these comments were made in
       @param reddit_user: A reddit user object to access data
       @param save_path: Working directory
       @param debug: Flag used for generating a local png and not uploading to Imgur
       @return: The formatted reply to the user ("NOT ENOUGH DATA" or link to image of pie graph on Imgur)
    """
    # Set to grab a certain number of comments from reddit...reddit wont return more than 2000
    comment_limit = 2000
    generated = reddit_user.get_comments(time='all', limit=comment_limit)

    # Only display top 6 subreddits
    num_top_subreddit = 6

    # Filter for category subreddits
    sub_name_len = 9

    # Stop Words are subreddits which do not contain important significance to be used in Search Queries.
    s = ('funny', 'pics', 'videos', 'giant', 'tall', 'aww', 'fuck', 'woahdude', 'modsupport', 'wtf', 'diy',
         'test', 'blog', 'gifs', 'promos', 'roastme', 'counting', 'askreddit', 'tifu', 'iama', 'porn')

    # Target Words are words which contain important significance to be used in Search Queries.
    t = ('play', 'do', 'watch', 'eat', 'want', 'love', 'need', 'into', 'thing', 'passion', 'hobby',
         'pastime', 'freetime', 'have', 'miss')

    total_comments = []
    counts = {}
    print('Analyzing interests...')

    # For each comment locate subreddit, categorize, and increment count
    for thing in generated:
        line = thing.body.split()
        sub = thing.subreddit.display_name.lower()
        if sub in counts:
            counts[sub] += 1
        elif sub not in s and len(sub) <= sub_name_len and '_' not in sub and sub.isalpha():
            counts[sub] = 0
        total_comments.append(line)

    answer = ''
    file_name = ''
    enough_data = True

    # Make a pie graph
    if len(counts) > 0:
        plt.figure(1, figsize=(6,6))
        # Remove subreddits with low counts
        removed_uncommon = {x:y for x,y in counts.items() if y!=0}

        # Order subreddits by count
        sorted_counts = OrderedDict(sorted(removed_uncommon.items(), key=lambda z: z[1], reverse=True))

        # Grab the top subreddits
        top = list(sorted_counts)[:num_top_subreddit]
        top_count = list(sorted_counts.values())[:num_top_subreddit]
        labels = top
        fracs = []
        summ = sum(top_count)
        for tc in top_count:
            fracs.append(round((tc/summ)*100))

        print('Creating pie graph...')
        plt.pie(fracs, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        plt.title(reddit_user.name, bbox={'facecolor':'0.8', 'pad':5})

        # Saves a png of the generated report
        file_name = os.path.join(save_path + str(reddit_user.name) + '_interests.png')
        plt.savefig(file_name)

    else:
        enough_data = False
        print('NOT ENOUGH DATA')

    # Upload image and remove local copy of png if enough data
    if not debug and enough_data:
        answer = upload.upload_image(file_name)
        os.remove(file_name)
    elif not enough_data:
        answer = "# NOT ENOUGH DATA"
    if debug:
        plt.show()

    return answer

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    interests(reddit_u, debug=True)
