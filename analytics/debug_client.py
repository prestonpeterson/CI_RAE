import time
import praw
from karma_breakdown import karma_breakdown
from word_count import word_count
from user_activity import user_activity


class DebugClient:

    def __init__(self):
        self.r = praw.Reddit('Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)')
        self.r.login(username='ci_rae', password='herpderp')
        self.already_done = []
        self.prawWords = ['ci_rae']

    def run(self):
        while True:
            subreddit = self.r.get_subreddit('test')
            for submission in subreddit.get_hot(limit=10):
                #flatten the comment tree forest to a list
                flat_comments = praw.helpers.flatten_tree(submission.comments)
                for comment in flat_comments:
                    has_praw = any(string in comment.body for string in self.prawWords)
                    # Test if it contains a PRAW-related question
                    if comment.id not in self.already_done and has_praw:
                        # print("Found post with user name", comment.author.user_name)
                        msg = '[PRAW related thread](%s)' % submission.short_link
                        comment_body_list = comment.body.split()
                        # command = comment_body_list[1]
                        user_name = comment.author

                        user_activity(user_name)
                        karma_breakdown(user_name)
                        word_count(user_name)

                        #comment.reply("ci_rae")
                        self.already_done.append(comment.id)
            time.sleep(3)

if __name__ == '__main__':
    dc = DebugClient()
    dc.run()
