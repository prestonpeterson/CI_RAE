from wordcloud import STOPWORDS
from collections import Counter
from operator import itemgetter


def subreddit_current_trend(subreddit, submission_limit=6, skip_more_comments=True):
    # A dictionary containing all the words in the comments
    # Key (String): the word used
    # Value (int): count of how many times the word was said
    counted_comments = {}
    # using stopwords from wordcloud to remove insignificant words ('The', 'at', etc.)
    stop_words = set(STOPWORDS)
    stop_words.add('*')
    stop_words.add('i')
    stop_words.add('>')
    # Get submissions from subreddit
    for submission in subreddit.get_hot(limit=submission_limit):
        # A list containing all the words in the comment
        words_in_comment = []

        # We also take into consideration the submission's text as well
        submission_text = ''.join([submission.title, ' ', submission.selftext])
        lines = submission_text.split()
        for x in range(len(lines)):
            words_in_comment.append(lines[x])
        # Populate words_in_comment from reddit submission
        for comment in submission.comments:
            if isinstance(comment, praw.objects.Comment):
                lines = comment.body.split()
                for x in range(len(lines)): words_in_comment.append(lines[x])
            else:
                if skip_more_comments:
                    continue
                #TODO: Impelement submission.replace_more_comments, this requires that you adhere to the API guidelines
        # Filter out stopwords
        words_in_comment = filter(lambda word: word not in stop_words, map(str.lower, words_in_comment))
        # Count words in words_in_comment and generate a dictionary <string Word, int Count>
        counted_comments.update(Counter(words_in_comment))

    # Remove entries that have a value of 0
    # removed_common = {x: y for x, y in counted_comments.items() if y != 'the'}
    # Sorts the dictionary by value, then reverses
    sorted_x = sorted(counted_comments.items(), key=itemgetter(1), reverse=True)
    top10 = sorted_x[:10]

    print(list(top10))
    return


if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    reddit = praw.Reddit(user_agent)
    reddit.login(username='ci_rae', password='herpderp')
    subreddit = reddit.get_subreddit('pokemongo') # pokemongo, LUL
    subreddit_current_trend(subreddit)
