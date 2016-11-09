# Phillip Porter
# 11/2/16

# snarkiness.py

import praw

# Sorted list child class of builtin list
# Requires that list be sorted or contains will fail to provide accurate results


class __sorted_list(list):
    def __contains__(self, item):
        first = 0
        last = len(self) - 1
        found = False

        if last >= 0:
            while first <= last and not found:
                index = first + ((last - first) // 2)

                if self[index] > item:
                    last = index - 1
                elif self[index] < item:
                    first = index + 1
                else:
                    found = True
        return found

# Computes snarkiness of user given use of profanity in comments


def snarkiness(reddit_user):
    profane_words = __sorted_list(['arse', 'arsehole', 'arserape', 'arsewipe', 'ass', 'asses', 'asshole', 'assholes',
                     'assramer', 'assrape', 'bastard', 'beastial', 'beastiality', 'beastility', 'bestial',
                     'bestiality', 'bitch', 'blowjob', 'blowjobs', 'bollock', 'bollocks', 'boobs', 'bullshit',
                     'butfuck', 'buttfuck', 'buttfucker', 'buttmonkey', 'chink', 'clamjouster', 'clit', 'cock',
                     'cocks', 'cockslap', 'cockslapped', 'cockslapping', 'cocksuck', 'cocksucked', 'cocksucker',
                     'cocksucking', 'cocksucks', 'crap', 'cum', 'cummer', 'cumming', 'cums', 'cumshot',
                     'cunilingus', 'cunillingus', 'cunnilingus', 'cunt', 'cuntalot', 'cuntfish', 'cunting',
                     'cuntlick', 'cuntlicker', 'cuntlicking', 'cuntree', 'cunts', 'cyberfuc', 'cyberfuck',
                     'cyberfucked', 'cyberfucker', 'cyberfuckers', 'cyberfucking', 'damn', 'dick', 'dickabout',
                     'dickaround', 'dickhead', 'dicking', 'dickwad', 'dickward', 'dildo', 'dildos', 'dirty-sanchez',
                     'donkeypunch', 'dyke', 'ejaculate', 'ejaculated', 'ejaculates', 'ejaculating', 'ejaculatings',
                     'ejaculation', 'fag', 'fagging', 'faggot', 'faggs', 'fagot', 'fagots', 'fags', 'fatass',
                     'feces', 'felatio', 'fellatio', 'ficken', 'fingerfuck', 'fingerfucked', 'fingerfucker',
                     'fingerfuckers', 'fingerfucking', 'fingerfucks', 'fistfuck', 'fistfucked', 'fistfucker',
                     'fistfuckers', 'fistfucking', 'fistfuckings', 'fistfucks', 'fuck', 'fucked', 'fucker',
                     'fuckers', 'fuckin', 'fucking', 'fuckings', 'fuckmaster', 'fuckme', 'fucks', 'fuckwit',
                     'fucky', 'fuk', 'fuks', 'futkretzn', 'gangbang', 'gangbanged', 'gangbangs', 'gash', 'gaysex',
                     'goddamn', 'goolies', 'guiena', 'hardcoresex', 'hell', 'helvete', 'honkey', 'horniest',
                     'horny', 'hotsex', 'injun', 'jack-off', 'jerk-off', 'jiz', 'jizm', 'kaffir', 'knobend',
                     'knobhead', 'kunilingus', 'lesbian', 'lesbo', 'lust', 'lusting', 'masturbat', 'milf',
                     'monkleigh', 'mothafuck', 'mothafucka', 'mothafuckas', 'mothafuckaz', 'mothafucked',
                     'mothafucker', 'mothafuckers', 'mothafuckin', 'mothafucking', 'mothafuckings', 'mothafucks',
                     'motherfuck', 'motherfucked', 'motherfucker', 'motherfuckers', 'motherfuckin', 'motherfucking',
                     'motherfuckings', 'motherfucks', 'muffdiver', 'muffmuncher', 'mummyporn', 'munter', 'muschi',
                     'nazis', 'niger', 'nigga', 'niggar', 'niggars', 'nigger', 'niggers', 'nutsack', 'ootzak',
                     'orgasim', 'orgasims', 'orgasm', 'orgasms', 'pendejo', 'penis', 'piss', 'pissed', 'pisser',
                     'pissers', 'pisses', 'pissin', 'pissing', 'pissoff', 'porn', 'porno', 'pornography', 'pornos',
                     'prick', 'pricks', 'pusies', 'pussies', 'pussy', 'pussys', 'pusy', 'pusys', 'puta', 'puto',
                     'queef', 'queer', 'qweef', 'schmuck', 'scrotum', 'shag', 'shagged', 'shemale', 'shit',
                     'shited', 'shitfull', 'shithead', 'shithole', 'shiting', 'shitings', 'shits', 'shitted',
                     'shitter', 'shitters', 'shitting', 'shittings', 'shitty', 'shity', 'shiz', 'slag', 'slut',
                     'sluts', 'smut', 'snatch', 'spacko', 'spank', 'spastic', 'spic', 'splooge', 'spunk', 'spunking',
                     'tits', 'twat', 'wank', 'wanked', 'wanker', 'wankered', 'wankers', 'wanking', 'whore'])

    comment_percent_threshold = .1

    comment_generator = reddit_user.get_comments(time='all', limit=None)
    profanity_dictionary = dict()

    user_name = reddit_user.name
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
