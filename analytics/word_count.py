import matplotlib.pyplot as plt
from operator import itemgetter
from collections import Counter
from imgur import upload
import numpy as np
import os


#TODO: Labels on the bottom are being cut off, looking for a solution
#TODO: Y Tick labels get squished together if a word count is high, implement scaling tick numbers
def word_count(reddit_user, save_path=''):
    # Set to grab a certain number of things from reddit...reddit wont return more than 1000
    thing_limit = 100
    # Stop Words are words which do not contain important significance to be used in Search Queries.
    s = ('all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should',
          'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor',
         'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves',
         'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by',
          'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their',
       'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with',
        'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then',
          'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how',
       'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once',
           'I', 'The')

    generated = reddit_user.get_comments(time='all', limit=thing_limit)

    total_comments = []
    for thing in generated:
        line = thing.body.split()
        for x in range(len(line)):
            total_comments.append(line[x])
    counted_comments = filter(lambda w: not w in s, total_comments)

    counted_comments = Counter(counted_comments)
    # remove entries that have a value of 0
    removed_common = {x:y for x,y in counted_comments.items() if y!='the'}
    #sorts the dictionary by value, then reverses
    sorted_x = sorted(removed_common.items(), key=itemgetter(1), reverse=True)

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

    ax.set_title("Top 20 most common words by: " + reddit_user.name)

    ax.set_xlabel("Word")
    ax.set_ylabel("Frequency", rotation='vertical')

    ax.set_xlim([0, len(sorted_range)])
    ax.set_ylim([0, max_y_tick])

    fig.tight_layout() # This is apparently supposed to give room to the x labels
    ax.axis('tight')

    ax.set_xticks(sorted_range)
    ax.set_yticks(range(max_y_tick))

    ax.set_xticklabels(sorted_keys, rotation='vertical')

    #saves a png of the generated report
    file_name = os.path.join(save_path + reddit_user.name + '_word_count.png')
    plt.savefig(file_name)
    image_link = upload.upload_image(file_name)

    # Remove local copy of png
    os.remove(file_name)

    return image_link
