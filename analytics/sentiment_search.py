import nltk
import yaml
import praw
import os
from math import trunc

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


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
        for file in files:
            file.close()
        # map(lambda x: x.close(), files)
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


def check_sentiment(splitter, postagger, dicttagger, comment, debug=False):
    splitted_sentences = splitter.split(comment.body.lower())
    pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
    dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
    score = calc_sentiment_score(dict_tagged_sentences)
    adjusted_score = score * (comment.score / 2)
    if debug:
        print('comment: ', comment.body)
        print('\tupvotes: ', comment.score)
        print('\tsentiment score: ', score)
        print('\tsentiment score adjusted: ', adjusted_score)
    return adjusted_score


def sentiment_search(agent, keyword, debug=True):
    # TODO: Add functionality for '--thorough' argument which increases thread limit and more_comments limit
    # TODO: Add mutex for this function
    keyword = keyword.lower()
    splitter = Splitter()
    postagger = POSTagger()
    thread_limit = 12
    more_comments_limit = 5
    more_comments_threshold = 2
    dicttagger = DictionaryTagger(
        ['../analytics/sentiment_dicts/positive.yml', '../analytics/sentiment_dicts/negative.yml',
         '../analytics/sentiment_dicts/inc.yml', '../analytics/sentiment_dicts/dec.yml',
         '../analytics/sentiment_dicts/inv.yml']
    )
    search = agent.search(keyword, limit=thread_limit, sort='top', subreddit='all', period='month')
    sentiment_score = int(0)
    for index, result in enumerate(search):
        print('***COMPUTING SENTIMENT SCORE.... {:2.0f}% COMPLETE***'.format((float(index / thread_limit) * 100)))
        try:
            result.replace_more_comments(limit=more_comments_limit, threshold=more_comments_threshold)
            if result.comments is not None:
                for comment in result.comments:
                    if type(comment) is praw.objects.Comment and keyword in comment.body.lower() and comment.score > 0:
                        sentiment_score += int(check_sentiment(splitter, postagger, dicttagger, comment, debug=debug))
        except Exception as e:
            print(e)

    if debug:
        print('*********\nFINAL SENTIMENT SCORE FOR KEYWORD "{}" = {}\n*********'.format(keyword, str(sentiment_score)))
    result_str = 'Sentiment Score ' + str(sentiment_score) + ': '
    if sentiment_score > 9000:  # this probably won't happen much
        result_str += '**IT\'S OVER 9000** '
    if sentiment_score >= 2000:
        result_str += '_**Overwhelmingly Positive**_'
    elif sentiment_score >= 1500:
        result_str += '**Extremely Positive**'
    elif sentiment_score >= 1000:
        result_str += '**Very Positive**'
    elif sentiment_score >= 500:
        result_str += '**Fairly Positive**'
    elif sentiment_score >= 200:
        result_str += '**Slightly Positive**'
    elif sentiment_score <= -2000:
        result_str += '_**Overwhelmingly Negative**_'
    elif sentiment_score <= -1500:
        result_str += '**Extremely Negative**'
    elif sentiment_score <= -1000:
        result_str += '**Very Negative**'
    elif sentiment_score <= -500:
        result_str += '**Fairly Negative**'
    elif sentiment_score <= -200:
        result_str += '**Slightly Negative**'
    else:  # 200 > sentiment_score > -200
        result_str += '**Neutral**'
    result_str += '*\n\n&nbsp;\n^(*^Based ^on ^Reddit ^users ^usage ^of ^search ^term ^{} ^over ^the ^past ^30 ^days)'.format(keyword)
    return result_str


if __name__ == '__main__':
    from bot.settings import user_agent

    client = praw.Reddit(user_agent)
    # print(sentiment_search(client, 'macbook', debug=True))
    # print(sentiment_search(client, 'skyrim', debug=True))
    print(sentiment_search(client, 'galaxy note 7', debug=True))
    # print(sentiment_search(client, 'nickelback', debug=True))
    # print(sentiment_search(client, 'game of thrones', debug=True))
    # print(sentiment_search(client, 'a;dslfkjz;ldfkjzx;lfkjaszd;flkj', debug=True))
