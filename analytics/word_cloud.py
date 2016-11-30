# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from imgur import upload
import os


def word_cloud(reddit_user, save_path='', debug=False):
    """Set to grab a certain number of things from reddit. Reddit wont return more than 1000
       @param reddit_user A reddit user object to access data
       @param save_path Used to generate link for generated image
       @param debug Used to set debug mode
       @return generated image link
    """

    # Stopwords from wordcloud
    s = set(STOPWORDS)
    s.add("one")

    generated = reddit_user.get_comments(time='all', limit=None)

    total_comments = str()
    for thing in generated:
        total_comments += thing.body
        total_comments += " "

    # Take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(scale=3, relative_scaling=.5, random_state=1, stopwords=s).generate(total_comments)
    plt.figure()
    plt.title(reddit_user.name + "'s image cloud")
    plt.imshow(wordcloud)
    plt.axis("off")

    # Saves a png of the generated report
    file_name = os.path.join(save_path + reddit_user.name + '_word_cloud.png')
    plt.savefig(file_name)

    # Remove local copy of png
    if not debug:
        image_link = upload.upload_image(file_name)
        os.remove(file_name)
        return image_link
    else:
        plt.show()
        os.remove(file_name)
        return file_name

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    word_cloud(reddit_u, debug=True)
