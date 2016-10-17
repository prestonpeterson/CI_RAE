import praw

class CIRAEHelp:
    def __init__(self, comment):
        self.comment = comment #comment object
    def ci_rae_help(self):
        user_name = (self.comment).author.name
        answer = ("Thanks for using CI_RAE, "+ user_name + "! Follwing the format \"/u/ci_rae <command>\", here is a list of commands that you can use:\n\n"
        "**user_activity**: generates a graph that shows when a user is most active\n\n"
        "**word_cloud**: generates a word cloud based on your comment history\n\n"
        "**word_count**: generates a graph that shows the words you used the most in your comment history\n\n"
        "**karma_breakdown**: generates a graph that shows your karma based on which subreddits you've submitted and commented on")
        (self.comment).reply(answer)
        print("Responded to command")