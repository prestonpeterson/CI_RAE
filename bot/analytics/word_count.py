import praw
import matplotlib.pyplot as plt
import numpy as np
import operator
from operator import itemgetter
from collections import Counter

# Per the reddit API, user agent should follow format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

r = praw.Reddit(user_agent=user_agent)

#Stop Words are words which do not contain important significance to be used in Search Queries.
s=('all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should',
    'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor',
    'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves',
    'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by',
    'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their',
    'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with',
    'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my', 'and', 'then',
    'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how',
    'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once',
    'I', 'The')

#set to grab a certain number of things from reddit...reddit wont return more than 1000
thing_limit = 100
user_name = input("Please Enter a user to get their top 20 most used words:\n")

user = r.get_redditor(user_name)

generated = user.get_comments(time='all', limit=None)

karma_by_subreddit = {}
total_comments = []
for thing in generated:
    line = thing.body.split()
    for x in range(len(line)):
        total_comments.append(line[x])
print(total_comments)
counted_comments = filter(lambda w: not w in s, total_comments)

counted_comments = Counter(counted_comments)
print(counted_comments)
# remove entries that have a value of 0
removed_common = {x:y for x,y in counted_comments.items() if y!='the'}
print(removed_common)
#sorts the dictionary by value, then reverses
sorted_x = sorted(removed_common.items(), key=operator.itemgetter(1), reverse=True)

#get just the keys into a sorted list, and trim to get the top 20
sorted_keys = list(map(itemgetter(0), sorted_x))
del sorted_keys[20:]

#get just the keys into a sorted values, and trim to get the top 20
sorted_values = list(map(itemgetter(1), sorted_x))
del sorted_values[20:]

fig = plt.figure()
plt.bar(range(len(sorted_values)), sorted_values, align='center')
plt.title("Top 20 most common words by: " + user_name)
plt.xlabel("Word")
plt.ylabel("Frequency", rotation='vertical')
plt.xticks(range(len(sorted_keys)), sorted_keys, rotation='vertical')
plt.tight_layout()
#saves a png of the generated report
plt.savefig(user_name+'_wordcount.png')
plt.show()
