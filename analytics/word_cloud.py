#to install wordcloud use command:
# pip3 install wordcloud
#to install natural language tool kit use command:
# pip3 install nltk
#then you need to download the corpus, fire up a python terminal
#>>> import nltk
#>>> nltk.download()

from PIL import Image
from os import path
import praw
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from nltk.corpus import stopwords


class CIWordCloud:
    def __init__(self,user_name):
        self.user_name = user_name

    def word_cloud(self):
        #stopwords from wordcloud
        s = set(STOPWORDS)

        # Per the reddit API, user agent should follow format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
        user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

        r = praw.Reddit(user_agent=user_agent)

        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        thing_limit = 1000
        # user_name = input("Please Enter a user to get their top 20 most used words:\n")

        user = r.get_redditor(self.user_name)

        generated = user.get_comments(time='all', limit=None)

        total_comments = str()
        for thing in generated:
            total_comments += thing.body
            total_comments += " "
        #filter out common stopwords using the nltk stopwords corpus
        filtered_comments = ' '.join([word for word in total_comments.split() if word not in (stopwords.words('english'))])

        # take relative word frequencies into account, lower max_font_size
        wordcloud = WordCloud(max_font_size=100, relative_scaling=.1, stopwords=s).generate(filtered_comments)
        plt.figure()
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        #plt.savefig("./wordcloud/"+user_name+"_wordcloud.png")
