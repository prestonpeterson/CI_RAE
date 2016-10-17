from PIL import Image
from os import path
import praw
import numpy as np
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS

class CIImageCloud:
    def __init__(self,user_name):
        self.user_name = user_name
    def image_cloud(self):

        #stopwords from wordcloud
        s = set(STOPWORDS)
        s.add("one")

        # Per the reddit API, user agent should follow format: <platform>:<app ID>:<version string> (by /u/<reddit username>)
        user_agent = ("Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)")

        r = praw.Reddit(user_agent=user_agent)

        #set to grab a certain number of things from reddit...reddit wont return more than 1000
        thing_limit = 1000
        #user_name = input("Please Enter a user to get their top 20 most used words:\n")

        user = r.get_redditor(self.user_name)

        generated = user.get_comments(time='all', limit=None)
        reddit_mask = np.arrayImage.open(path.join("./", "reddit.png"))

        total_comments = str()
        for thing in generated:
            total_comments += thing.body
            total_comments += " "

        # take relative word frequencies into account, lower max_font_size
        wordcloud = WordCloud(scale=3, mask=reddit_mask, relative_scaling=.5, random_state=1, stopwords=s).generate(total_comments)
        plt.figure()
        plt.title(self.user_name + "'s image cloud")
        plt.imshow(wordcloud)
        plt.axis("off")
        plt.show()
        #plt.savefig(self.user_name+"_imagecloud.png")
        Image.close(path.join("./", "reddit.png"))
