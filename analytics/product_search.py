import nltk
import yaml
import praw
yaml.load("dict:")

class Splitter(object):
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):
    def __init__(self):
        pass

    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos


# class DictionaryTagger from http://fjavieralba.com/basic-sentiment-analysis-with-python.html
class DictionaryTagger(object):
    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])





def product_search(client, keyword):
    splitter = Splitter()
    postagger = POSTagger()
    dicttagger = DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])


    derp = client.search(keyword, limit=1000, sort='relevance', subreddit='all', period='1 year')
    for herp in derp:
            print(herp.subreddit)
            print(dir(herp))
            for comment in herp.comments:
                if type(comment) is praw.objects.Comment and keyword in comment.body:
                    splitted_sentences = splitter.split(comment.body)
                    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
                    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
                    print('comment: ', comment.body)
                    quality = sentiment_score(dict_tagged_sentences)
                    print('quality: ', quality)
            break


#
#
# import nltk
# import nltk.tokenize
# # nltk.download('all-corpora')
# # nltk.download('tokenizers')
# from nltk.corpus import sentiwordnet as swn
#
# def product_search(reddit_client, keyword):
#     def check_qualitativeness(comment_body):
#         # nltk_tokenizer = nltk.data.load(comment_body)
#         sentences = nltk.word_tokenize(comment_body)
#         nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()
#         tokenized = [nltk_tokenizer.tokenize(sent) for sent in sentences]
#         pos = [nltk.pos_tag(sentence) for sentence in sentences]
#         print('pos = ', pos)
#         pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
#         return pos
#         # token = nltk.word_tokenize(comment_body)
#         # tagged = nltk.pos_tag(token)
#         # return 1
#         # breakdown = swn.sentisynset('comment.body')
#         # print(breakdown)
#     """
#     pull top x threads from 'all' subreddit
#     :param reddit_client:
#     :param keyword:
#     :param subreddit:
#     :return:
#     """
#     derp = client.search(keyword, limit=1000, sort='relevance', subreddit='all', period='1 year')
#     i = 1
#     dicttagger = DictionaryTagger(['dicts/positive.yml', 'dicts/negative.yml'])
#
#     dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
#     """
#     ['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattr__',
#      '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__',
#      '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__',
#      '__unicode__', '__weakref__', '_api_link', '_comment_sort', '_comments', '_comments_by_id',
#      '_extract_more_comments', '_get_json_dict', '_has_fetched', '_info_url', '_insert_comment', '_methods',
#      '_orphaned', '_params', '_populate', '_post_populate', '_replaced_more', '_underscore_names', '_uniq',
#      '_update_comments', 'add_comment', 'approve', 'approved_by', 'archived', 'author', 'author_flair_css_class',
#      'author_flair_text', 'banned_by', 'clear_vote', 'clicked', 'comments', 'contest_mode', 'created', 'created_utc',
#      'delete', 'distinguish', 'distinguished', 'domain', 'downs', 'downvote', 'edit', 'edited', 'from_api_response',
#      'from_id', 'from_json', 'from_url', 'fullname', 'get_duplicates', 'get_flair_choices', 'gild', 'gilded',
#      'has_fetched', 'hidden', 'hide', 'hide_score', 'id', 'ignore_reports', 'is_self', 'json_dict', 'likes',
#      'link_flair_css_class', 'link_flair_text', 'lock', 'locked', 'mark_as_nsfw', 'media', 'media_embed', 'mod_reports',
#      'name', 'num_comments', 'num_reports', 'over_18', 'permalink', 'quarantine', 'reddit_session', 'refresh',
#      'removal_reason', 'remove', 'replace_more_comments', 'report', 'report_reasons', 'save', 'saved', 'score',
#      'secure_media', 'secure_media_embed', 'select_flair', 'selftext', 'selftext_html', 'set_contest_mode', 'set_flair',
#      'set_suggested_sort', 'short_link', 'spoiler', 'stickied', 'sticky', 'subreddit', 'subreddit_id', 'suggested_sort',
#      'thumbnail', 'title', 'undistinguish', 'unhide', 'unignore_reports', 'unlock', 'unmark_as_nsfw', 'unsave',
#      'unset_contest_mode', 'unsticky', 'ups', 'upvote', 'url', 'user_reports', 'visited', 'vote']
#      """
#     positive_qualities = ['good', 'great', ]
#     print(dir(nltk))
#
#     for herp in derp:
#         print(herp.subreddit)
#         print(i)
#         i += 1
#         print(dir(herp))
#         for comment in herp.comments:
#             if type(comment) is praw.objects.Comment and keyword in comment.body:
#                 print('comment: ', comment.body)
#                 quality = check_qualitativeness(comment.body)
#                 print(quality)
#         break
#
#
if __name__ == '__main__':
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)
    product_search(client, 'macbook')
    # print(result)
    # text = "The macbook is not good. I love it tho"
    # text2 = "The macbook is the greatest thing ever. I can't get enough of it"
    # text3 = "The macbook is garbage. It is a steaming pile of trash"


