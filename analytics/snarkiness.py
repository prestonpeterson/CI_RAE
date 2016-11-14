# @author:   Phillip Porter
# @date:     11/3/16
# @filename: snarkiness.py

import praw
from analytics.profanity import *

"""
A function to measure the profanity used in all of a user's comments, then produces
a report formatted to be displayed on the reddit website in a comment to the
user who requested the report

@:param reddit_user instance of Redditor class from praw.objects
@:return String value containing the formatted report
 """


def snarkiness(reddit_user):
    # Represents percent value of comments that contain profanity for user to be labeled
    # "Snarky"
    comment_percent_threshold = .1

    # Iterable container holding all comments for reddit user
    comment_generator = reddit_user.get_comments(time='all', limit=None)
    # Dictionary for words used by the reddit user
    profanity_dictionary = dict()

    # Name string for user
    user_name = reddit_user.name

    # Global counts for profane words and comments
    count_words_profane = 0
    count_words = 0
    count_comments_profane = 0
    count_comments = 0
    longest_word = 0

    # Iterate over all comments
    for comment in comment_generator:
        # Split up comment into word list
        commentText = comment.body.lower().split(' ')

        # Assume comment is not profane
        profane_comment = False
        for word in commentText:
            if word in profane_words:
                # Set profanity flag
                profane_comment = True
                # Increment profanity count
                count_words_profane += 1
                # Check dictionary
                if word in profanity_dictionary:
                    profanity_dictionary[word] += 1
                else:
                    profanity_dictionary[word] = 1
                    # Update longest word length
                    longest_word = max(longest_word, len(word))
            # Update total word count
            count_words += 1
        # Update comment counts
        if profane_comment:
            count_comments_profane += 1
        count_comments += 1

    # Begin report text
    result = str()
    result += "Here is what " + user_name + " has been saying:\n\n"
    result += "/////////////////////////////////////////\n\n"

    # Produce line for each swear word in dictionary
    # Format as follows: [WORD] AUTO_WIDTH:COUNT
    for key in profanity_dictionary:
        result += ("{0:<" + str(longest_word + 1) + "}:{1!s}\n\n").format(key,profanity_dictionary[key])

    result += "Profane words used: " + str(count_words_profane)
    result += "\n\nTotal words used: " + str(count_words)

    if count_comments_profane / count_comments > comment_percent_threshold:
        result += "\n\nEyyyy, \"" + user_name + "\" is snarky!"
    else:
        result += "\n\nEyyyy, \"" + user_name + "\" isn't snarky!"

    return result

# Testing module
if __name__ == "__main__":
    import sys
    from bot.settings import user_agent
    r = praw.Reddit(user_agent=user_agent)

    print('Please enter the name of the user to check for snarkiness: ')
    user_name = sys.stdin.readline()
    user_name = user_name[:-1]

    print(snarkiness(r.get_redditor(user_name)))
