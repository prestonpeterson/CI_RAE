"""@package docstring
This function returns a comment back to the user with a list of commands the user can submit as a comment
"""
def ci_rae_help(redditor):
    """@param redditor: A redditor object. Used to access username and to reply back to comment.
       @return: The formated reply to the user
    """
    user_name = redditor.name
    answer = ("Thanks for using CI_RAE, "+ user_name + "! Follwing the format \"/u/ci_rae <command> <target>\", here is a list of commands that you can use:\n\n"
    "**user_activity**: Generates a graph that shows when a user is most active.\n\n"
    "**word_cloud**: Generates a word cloud based on your comment history.\n\n"
    "**word_count**: Generates a graph that shows the words you used the most in your comment history.\n\n"
    "**karma_breakdown**: Generates a graph that shows your karma based on which subreddits you've submitted and commented on.\n\n"
    "**locations**: Generates a list of locations you have mentioned such as countries and states (currently, only U.S. states are listed).\n\n"
    "**user_interests**: Generates a graph that shows what interests the user the most.\n\n"
    "**sentiment_search**: Scans Reddit user's usage of given target product or terms, performs a linguistic analysis to determine Reddit's overall sentiment on the subject: good, bad, or otherwise.\n\n"
    "**snarkiness**: Returns a score based on how often the user says profanity.\n\n"
    "**best_worst**: Returns a user's comment and submission with the highest score, and the comment and submission with the lowest score.")
    return answer

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    bestworst = ci_rae_help(reddit_u)
    print(bestworst)


