import praw
"""@package docstring
This function returns a comment back to the user with a list of commands the user can submit as a comment
"""
def ci_rae_help(comment):
    """@param comment A reddit Comment object. Used to access username and to reply back to comment."""
    user_name = comment.author.name
    answer = ("Thanks for using CI_RAE, "+ user_name + "! Follwing the format \"/u/ci_rae <command> <target>\", here is a list of commands that you can use:\n\n"
    "**user_activity**: generates a graph that shows when a user is most active\n\n"
    "**word_cloud**: generates a word cloud based on your comment history\n\n"
    "**word_count**: generates a graph that shows the words you used the most in your comment history\n\n"
    "**karma_breakdown**: generates a graph that shows your karma based on which subreddits you've submitted and commented on\n\n"
    "**image_cloud**: generates a word cloud shaped as Snoo, reddit's mascot.")
    "**user_interests: generates a graph that shows what interests the user the most\n\n"
    return answer