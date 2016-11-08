import matplotlib.pyplot as plt
from operator import itemgetter
from collections import Counter
from imgur import upload
import numpy as np
import os
import string
from collections import OrderedDict
from pylab import *


def interests(reddit_user, save_path='', debug=False):
    # Set to grab a certain number of things from reddit...reddit wont return more than 1000
    thing_limit = 1000
    sub_name_len = 8
    #nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    aww_sub = ('aww', 'pets')
    # Stop Words are words which do not contain important significance to be used in Search Queries.
    s = ('giant', 'tall', 'woah', 'aww', 'mod', 'all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should',
          'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor',
         'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves',
         'out', 'what', 'for', 'while', 'does', 'above', 'between', 'be', 'we', 'who', 'were', 'here', 'hers', 'by',
          'on', 'about', 'of', 'against', 'or', 'own', 'yourself', 'down', 'your', 'from', 'her', 'their',
       'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with',
        'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then', 'itself',
         'at', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why',
         'off', 'yours', 'so', 'the', 'having', 'once', 'the', 'jerk', 'un', 'videos', 'pics', 'wtf', 'gifs', 'funny', 'woahdude', 'diy')

    # Target Words are words which contain important significance to be used in Search Queries.
    t = ('play', 'do', 'watch', 'eat', 'want', 'love', 'need', 'into', 'thing', 'passion', 'hobby',
         'pastime', 'freetime', 'have', 'miss')

    generated = reddit_user.get_comments(time='all', limit=thing_limit)
    total_comments = []
    counts = {}

    # Analytics and generate pie graph with interests

    for thing in generated:
        line = thing.body.split()
        #for x in t:
            #if x in line:
        sub = thing.subreddit.display_name.lower()
        if sub in counts:
            counts[sub] += 1
        elif sub not in counts and len(sub) <= sub_name_len and '_' not in sub and sub not in s:
            counts[sub] = 0
        total_comments.append(line)

    # make a square figure and axes
    figure(1, figsize=(6,6))

    if len(counts) > 0:
        removed_uncommon = {x:y for x,y in counts.items() if y!=0}
        sorted_counts = OrderedDict(sorted(removed_uncommon.items(), key=lambda z: z[1], reverse=True))
        top = list(sorted_counts)[:6]
        top_count = list(sorted_counts.values())[:6]
        print('Analyzed interests')

        labels = top
        fracs = []
        summ = sum(top_count)
        for tc in top_count:
            fracs.append(round((tc/summ)*100))

        print('Creating pie graph')

        pie(fracs, labels=labels, autopct='%1.1f%%', shadow=False, startangle=90)
        # The default startangle is 0, which would start
        # the Frogs slice on the x-axis.  With startangle=90,
        # everything is rotated counter-clockwise by 90 degrees,
        # so the plotting starts on the positive y-axis.

        title(reddit_user.name, bbox={'facecolor':'0.8', 'pad':5})

    else:
        print('Not enough data')
        title(reddit_user.name + ' - NOT ENOUGH DATA', bbox={'facecolor':'0.8', 'pad':5})

    #saves a png of the generated report
    file_name = os.path.join(save_path + reddit_user.name + '_interests.png')
    plt.savefig(file_name)

    # Remove local copy of png
    if not debug:
         image_link = upload.upload_image(file_name)
         os.remove(file_name)
    else:
         image_link = ''

    return image_link

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('gallowboob')
    interests(reddit_u, debug=True)
