import matplotlib.pyplot as plt
from imgur import upload
from collections import OrderedDict
from pylab import *
import os


def interests(reddit_user, save_path='', debug=False):
    # Set to grab a certain number of comments from reddit...reddit wont return more than 2000
    comment_limit = 2000
    generated = reddit_user.get_comments(time='all', limit=comment_limit)

    # Only display top 6 subreddits
    num_top_subreddit = 6

    # Filter for category subreddits
    sub_name_len = 9

    # Stop Words are subreddits which do not contain important significance to be used in Search Queries.
    s = ('funny', 'pics', 'videos', 'giant', 'tall', 'aww', 'fuck', 'woahdude', 'modsupport', 'wtf', 'diy',
         'test', 'blog', 'gifs', 'promos', 'roastme', 'counting', 'askreddit')

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
        elif sub not in s and len(sub) <= sub_name_len and '_' not in sub:
            counts[sub] = 0
        total_comments.append(line)

    answer = ''
    enough_data = True

    # Make a pie graph
    if len(counts) > 0:
        figure(1, figsize=(6,6))
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

        pie(fracs, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        # The default startangle is 0, which would start
        # the Frogs slice on the x-axis.  With startangle=90,
        # everything is rotated counter-clockwise by 90 degrees,
        # so the plotting starts on the positive y-axis.

        title(reddit_user.name, bbox={'facecolor':'0.8', 'pad':5})

    else:
        enough_data = False
        print('NOT ENOUGH DATA')
        title(reddit_user.name + ' - NOT ENOUGH DATA', bbox={'facecolor':'0.8', 'pad':5})

    # Saves a png of the generated report
    file_name = os.path.join(save_path + reddit_user.name + '_interests.png')
    plt.savefig(file_name)

    # Remove local copy of png
    if not debug and enough_data:
        answer = upload.upload_image(file_name)
        os.remove(file_name)
    elif not enough_data:
        answer = "# NOT ENOUGH DATA"

    return answer

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    interests(reddit_u, debug=True)
