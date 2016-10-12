import time

import praw

from bot.analytics.word_cloud import CIWordCloud

r = praw.Reddit('Ubuntu 16.04:CI-RAE:V0.1 (by /u/giantmatt)')
r.login(username='ci_rae', password='herpderp')
already_done = []

prawWords = ['ci_rae']
while True:
    subreddit = r.get_subreddit('test')
    for submission in subreddit.get_hot(limit=10):

        #flatten the comment tree forest to a list
        flat_comments = praw.helpers.flatten_tree(submission.comments)
        for comment in flat_comments:
            has_praw = any(string in comment.body for string in prawWords)
            # Test if it contains a PRAW-related question
            if comment.id not in already_done and has_praw:
                # print("Found post with user name", comment.author.user_name)
                msg = '[PRAW related thread](%s)' % submission.short_link
                comment_body_list = comment.body.split()
                # command = comment_body_list[1]
                user_name = comment.author

                wc = CIWordCloud(user_name)
                wc.word_cloud()

                comment.reply("ci_rae")
        already_done.append(comment.id)
    time.sleep(3)
