import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import os


def word_cloud(reddit_user, save_path=''):
    # Set to grab a certain number of things from reddit...reddit wont return more than 1000
    thing_limit = 1000

    # Stopwords from wordcloud
    s = set(STOPWORDS)
    s.add("one")

    generated = reddit_user.get_comments(time='all', limit=None)

    total_comments = str()
    for thing in generated:
        total_comments += thing.body
        total_comments += " "

    # take relative word frequencies into account, lower max_font_size
    wordcloud = WordCloud(scale=3, relative_scaling=.5, random_state=1, stopwords=s).generate(total_comments)
    plt.figure()
    plt.title(reddit_user.name + "'s image cloud")
    plt.imshow(wordcloud)
    plt.axis("off")

    # Saves a png of the generated report
    file_name = os.path.join(save_path + reddit_user.name + '_word_cloud.png')
    plt.savefig(file_name)
    return file_name
