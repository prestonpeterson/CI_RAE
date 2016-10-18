import praw

class CIHelp:
    def __init__(self, comment):
        self.comment = comment #comment object
    def help(self):
        user_name = (self.comment).author.name
        answer = ("Thanks for using CI_RAE, "+ user_name + "! Follwing the format \"/u/ci_rae <command> <user>\", here is a list of commands that you can use:\n\n"
        "**user_activity**: generates a graph that shows the time of day the user is most active\n\n"
        "**word_cloud**: generates a word cloud based on the user's comment history\n\n"
        "**image_cloud**: generates a masked image cloud based on the user's comment history\n\n"
        "**word_count**: generates a graph that shows the words used the most in the user's comment history\n\n"
        "**karma_breakdown**: generates a graph that shows the user's top 20 posts, broken down by subreddit")
        (self.comment).reply(answer)
        print("Responded to command")