from wordcloud import STOPWORDS
from collections import Counter
from operator import itemgetter


def subreddit_current_trend(subreddit, skip_more_comments=True):
    # A dictionary containing all the words in the comments
    # Key (String): the word used
    # Value (int): count of how many times the word was said
    counted_comments = {}
    # using stopwords from wordcloud to remove insignificant words ('The', 'at', etc.)
    stop_words = set(STOPWORDS)

    for submission in subreddit.get_hot(limit=None):
        # A list containing all the words in the comment
        words_in_comment = []
        # Populate words_in_comment
        for comment in submission.comments:
            lines = comment.body.split()
            for x in range(len(lines)):
                words_in_comment.append(lines[x])

        # Filter out stopwords
        words_in_comment = filter(lambda word: word not in stop_words, words_in_comment)
        # Count words in words_in_comment and generate a dictionary <string Word, int Count>
        counted_comments.update(Counter(words_in_comment))

    # Remove entries that have a value of 0
    removed_common = {x: y for x, y in counted_comments.items() if y != 'the'}
    # Sorts the dictionary by value, then reverses
    sorted_x = sorted(removed_common.items(), key=itemgetter(1), reverse=True)

    print(list(sorted_x))
    return


if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    reddit = praw.Reddit(user_agent)
    reddit.login(username='ci_rae', password='herpderp')
    subreddit = reddit.get_subreddit('pokemongo')
    subreddit_current_trend(subreddit)
