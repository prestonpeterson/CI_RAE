# @author:   Phillip Porter
# @date:     11/3/16
# @filename: profanity

"""
Class override for built-in list
Overrides performance of __contains__ function
"""


class __sorted_list(list):
    """
    @:override __contains__ New version runs faster, and requires all contents to be sorted
    """
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


# sorted_list of profane words

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
