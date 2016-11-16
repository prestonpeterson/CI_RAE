# CI_RAE
Channel Islands Reddit Analytics Bot

Requirements:
  OS: Linux
  
  Python3, to install: `sudo apt-get install python3`
  
  pip3 to install dependencies: `sudo apt-get install python3-pip`
  
  Command to install dependencies (from CI_RAE directory): `pip3 install -r requirements.txt`

To run the bot, run bot_client.py in the CI_RAE/bot/ directory.

Bot will connect to reddit and listen for a command.  To create a command for the bot, sign up for a reddit account and post a comment anywhere with the following format:

/u/ci_rae <command> <target>

Commands are as follows:

  user_activity: Generates a graph that shows what time a user is most active.
  
  user_interests: Generates a graph that shows a pie chart based on what categories a user has expressed interest in.
  
  best_worst: Reports highest and lowest scoring comment for user.
  
  word_cloud: Generates a word cloud based on the user’s comment history.
  
  word_count: Generates a graph that shows the words you used the most in your comment history.
  
  karma_breakdown: Generates a graph that shows your total karma for the top 20 subreddits you have submitted in.
  
  snarkiness: Generates a report on what profanity a user has posted in comments.
  
  locations: Generates a list of locations the user has mentioned such as countries and states (currently limited to US).
  
  sentiment_search: Generates a report on user sentiment relating to a given search term.

A target can be a user or in the case of sentiment_search, a search term.
