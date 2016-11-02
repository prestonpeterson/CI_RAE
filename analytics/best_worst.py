def best_worst(reddit_user):
    """@param comment A reddit Comment object to reply to.
       @param reddit_user A reddit user object
    """
    comment_block = [] #list to prepare reply
    #account = reddit_client.get_redditor(self.user_name)

    #get top comment
    top_comment = reddit_user.get_comments(limit=1, sort='top')
    for comment in top_comment:
        top_score = str(comment.score)
        comment_block.append("## BEST COMMENT\n\n>"+comment.body+"    \n\nScore: **"+ top_score +"**")

    #get worst comment
    worst_comment = reddit_user.get_comments(limit=1, sort='controversial')
    for bad_comment in worst_comment:
        worst_score = str(bad_comment.score)
        comment_block.append("## WORST COMMENT\n\n>"+bad_comment.body+"    \n\nScore: **"+ worst_score +"**")

    #get top submission
    top_submission = reddit_user.get_submitted(limit=1, sort='top')
    for submission in top_submission:
        link = submission.permalink
        submission_score = str(submission.score)
        comment_block.append("Your [top submission]("+ link + ") has a score of **"+ submission_score +"**")

    #get worst submission
    worst_submission = reddit_user.get_submitted(limit=1, sort='controversial')
    for submission in worst_submission:
        link = submission.permalink
        submission_score = str(submission.score)
        comment_block.append("Your [worst submission]("+ link + ") has a score of **"+ submission_score +"**")

    answer = "\n\n***\n\n".join(comment_block)
    print("'best_worst() function successfully called'") #debug purposes
    return answer

if __name__ == '__main__':
    import praw
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    reddit_u = client.get_redditor('giantmatt')
    bestworst = best_worst(reddit_u)
    print(bestworst)