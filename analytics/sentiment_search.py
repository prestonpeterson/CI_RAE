# \author Mattias Huber, Preston Peterson, Phillip Porter, Heather Bradfield, Zoltan Batoczki, Jesus Bamford
# \copyright GNU Public License.

import nltk
import yaml
import praw

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


# Class Splitter derived from http://fjavieralba.com/basic-sentiment-analysis-with-python.html
class Splitter(object):
    """
    Uses Natural Language Toolkit to split a paragraph into a list of sentences
    """
    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        @param text a paragraph of text
        @return a list of lists of tokenized sentences
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):
    """
    Class POSTagger derived from http://fjavieralba.com/basic-sentiment-analysis-with-python.html
    Uses Natural Language Toolkit to categorize words into types (tags)
    """
    def __init__(self):
        pass

    def pos_tag(self, sentences):
        """
        @param sentences list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        @return a list of lists of tagged tokens
        Each tagged tokens has a form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """
        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        # adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos


class DictionaryTagger(object):
    """
    Class DictionaryTagger derived from http://fjavieralba.com/basic-sentiment-analysis-with-python.html
    Uses dictionaries of word associations to tag sentences with qualitative values
    """
    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        for file in files:
            file.close()
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            if curr_dict is not None:
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
        @return the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while i < N:
            j = min(i + self.max_key_size, N)  # avoid overflow
            tagged = False
            while j > i:
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    # self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token:  # if the tagged literal is a single token, conserve its previous taggings:
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
    if sentiment == 'positive':
        return 1
    if sentiment == 'negative':
        return -1
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


def calc_sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])


def check_sentiment(splitter, postagger, dicttagger, comment, search_terms, debug=False):
    terms = search_terms.lower().split(' ')
    sentences = comment.body.lower()
    for term in terms:
        sentences = sentences.replace(term, '')
    splitted_sentences = splitter.split(sentences)
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    score = calc_sentiment_score(dict_tagged_sentences)
    adjusted_score = (score/2) * comment.score
    if debug:
        print('comment: ', comment.body)
        print('\tupvotes: ', comment.score)
        print('\tsentiment score: ', score)
        print('\tsentiment score adjusted: ', adjusted_score)
    return adjusted_score


def sentiment_search(agent, search_term, debug=False):
    # TODO: Add functionality for '--thorough' argument which increases thread limit and more_comments limit
    # TODO: Add mutex for this function
    splitter = Splitter()
    postagger = POSTagger()
    thread_limit = 50
    dicttagger = DictionaryTagger(
        ['../analytics/sentiment_dicts/positive.yml', '../analytics/sentiment_dicts/negative.yml',
         '../analytics/sentiment_dicts/inc.yml', '../analytics/sentiment_dicts/dec.yml',
         '../analytics/sentiment_dicts/inv.yml']
    )
    search = agent.search(search_term, limit=thread_limit, sort='relevance', subreddit='all', period='month')
    sentiment_score = 0
    total_sentiment = 0
    for index, result in enumerate(search):
        print('***COMPUTING SENTIMENT SCORE.... {:2.0f}% COMPLETE***'.format((float(index / thread_limit) * 100)))
        try:
            if abs(sentiment_score) <= 20:
                # expand search
                more_comments_limit = 15
                more_comments_threshold = 0
            else:
                more_comments_limit = 5
                more_comments_threshold = 1
            # result.replace_more_comments(limit=more_comments_limit, threshold=more_comments_threshold)
            flattened_comments = praw.helpers.flatten_tree(result.comments)
            if result.comments is not None:
                for comm in flattened_comments:
                    if type(comm) is praw.objects.Comment and search_term.lower() in comm.body.lower() and comm.score > 0:
                        result = check_sentiment(splitter, postagger, dicttagger, comm, search_term, debug=debug)
                        sentiment_score += result
                        total_sentiment += abs(result)
        except Exception as e:
            print(e)

    if debug:
        print('*********\nFINAL SENTIMENT SCORE FOR KEYWORD "{}" = {}\n*********'.format(search_term, str(sentiment_score)))
        print('*********\nTOTAL SENTIMENT = {}\n**********'.format(total_sentiment))

    if total_sentiment == 0:
        result_str = "Insufficient data"
        sentiment_percent = 101
    else:
        sentiment_percent = int(float(sentiment_score / total_sentiment) * 100)
        result_str = '### Sentiment Score ' + str(int(sentiment_percent)) + ': '
    if sentiment_percent != 101:
        if sentiment_percent >= 65:
            result_str += '_Overwhelmingly Positive_'
        elif sentiment_percent >= 50:
            result_str += '_Extremely Positive_'
        elif sentiment_percent >= 35:
            result_str += '_Mostly Positive_'
        elif sentiment_percent >= 15:
            result_str += '_Fairly Positive_'
        elif sentiment_percent >= 5:
            result_str += '_Slightly Positive_'
        elif sentiment_percent <= -65:
            result_str += '_Overwhelmingly Negative_'
        elif sentiment_percent <= -50:
            result_str += '_Extremely Negative_'
        elif sentiment_percent <= -35:
            result_str += '_Mostly Negative_'
        elif sentiment_percent <= -15:
            result_str += '_Fairly Negative_'
        elif sentiment_percent <= -5:
            result_str += '_Slightly Negative_'
        else:
            result_str += 'Neutral**'
    search_term = search_term.split(' ')
    result_str += '*\n***\n&nbsp;\n^(*^Based ^on ^Reddit ^users ^usage ^of ^search ^term ^`{}` ^over ^the ^past ^30 ^days)'.format('` ^`'.join(search_term))
    return result_str


if __name__ == '__main__':
    """
    Unit tests
    """
    from bot.settings import user_agent
    client = praw.Reddit(user_agent)

    # print(sentiment_search(client, 'macbook', debug=True))
    # print(sentiment_search(client, 'skyrim', debug=True))
    # print(sentiment_search(client, 'galaxy note 7', debug=True))
    # print(sentiment_search(client, 'game of thrones', debug=True))
    print(sentiment_search(client, 'breaking bad', debug=True))
    # print(sentiment_search(client, 'game of thrones', debug=True))
    # print(sentiment_search(client, 'a;dslfkjz;ldfkjzx;lfkjaszd;flkj', debug=True))
