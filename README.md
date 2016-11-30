# CI_RAE
Channel Islands Reddit Analytics Bot

## Reddit Analytics Engine developed by students from CSU Channel Islands
## Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# Copyright GNU Public License.
### The purpose of this engine is to tap into the data goldmine that is Reddit.com. Reddit is a massive online forum and social network platform that hosts immense amounts of publicly available user data.    
### The Engine is also able to take user_input directly from comments posted on Reddit. Comments attempting to signal the Engine must begin with the string `/u/ci_rae`

> To view the complete source code documentation, clone the repo and open CI_RAE/doxygen/html/index.html in your preferred internet browser.

#### Input syntax: `/u/ci_rae command target`

### Analytics currently offered by CI_RAE:
* `user_activity`: Generates a graph that shows when a user is most active.
* `word_cloud`: Generates a word cloud based on your comment history.
* `word_count`: Generates a graph that shows the words you used the most in your comment history.
* `karma_breakdown`: Generates a graph that shows your karma based on which subreddits you've submitted and commented on.
* `locations`: Generates a list of locations you have mentioned such as countries and states (currently, only U.S. states are listed).
* `user_interests`: Generates a graph that shows what interests the user the most.
* `sentiment_search`: Scans Reddit user's usage of given target product or terms, performs a linguistic analysis to determine Reddit's overall sentiment on the subject: good, bad, or otherwise.
* `snarkiness`: Returns a score based on how often the user says profanity.
* `best_worst`: Returns a user's comment and submission with the highest score, and the comment and submission with the lowest score.
A target can be a user or in the case of sentiment_search, a search term.

---

#### Requirements:
* OS: Linux, OSX, or Windows
* Python3, to install: `sudo apt-get install python3`
* pip3 to install dependencies: `sudo apt-get install python3-pip`
* Command to install dependencies (from CI_RAE directory): `pip3 install -r requirements.txt`

To run the bot, run bot_client.py in the CI_RAE/bot/ directory.

Bot will connect to reddit and listen for a command.  To create a command for the bot, sign up for a reddit account and post a comment anywhere with the following format:

#### Dashboard:
* First install jupyter notebook: `sudo pip3 install jupyter`
* Then run in terminal: `jupyter notebook`
* By default, a local server will begin running on localhoast:8888
* Open a browser and type `localhost:8888`
* Navigate to and run the file `Channel Islands Reddit Analytics Engine Dashboard.ipynb`
* Make sure the script `jupyter_rae.py` is in the same directory as the .ipynb file
* Click on the cell that says `%run jupyter_rae.py`, and hit shift+enter in order to run
* Enter a redditor user name in the text box, then click on which analytics module you wish to run



