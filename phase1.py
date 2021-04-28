import os
import nltk
from Stemmer import *
from Lemmatizer import *
from Normalizer import *
import numpy as np
import collections

class Appearance:

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


from heapq import heappop, heappush


def heap_sort(array):
    heap = []
    for element in array:
        heappush(heap, element)

    ordered = []

    while heap:
        ordered.append(heappop(heap))

    return ordered


def read_data(path):
    contents = []
    for filename in os.listdir(path):
        data = open(path + '/' + filename, 'r', encoding='utf8').read()
        filename = re.sub('\D', "", filename)
        contents.append({
            'docId': (int(filename)),
            'text': data
        })
    return contents


def tokenize_and_remove_punctuations(s):
    single_chars = ['»', '.', '«', '،', '؟', '"', '#', ')', '(', '*', ',', '-', '/', ':', '[', ']', '،', '?', '…', '۰',
                    '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '-', '+', '=', '@', '$', '$', '%', '^', '&', '-', '_',
                    '{', '}', '\'', '/', ';', '  ', '>', '<', '•', '٪', '؛']
    text = s.strip(u'\xa0\u200c \t\n\r\f\v')
    text = text.replace('\n', ' ')
    text = Normalizer().normalize(text)
    for sc in single_chars:
        if text.__contains__(sc):
            text = text.replace(sc, ' ')
    terms = text.split(' ')
    for term in terms:
        if term.__eq__(''):
            terms.remove(term)
        if term.isnumeric():
            terms.remove(term)
    return terms


def get_stopwords():
    stop_words = [word for word in open('stopwords.txt', 'r', encoding='utf8').read().split('\n')]
    return stop_words


def stem_words(tokens):
    stemmer = Stemmer()
    stemmed_words = [stemmer.stem(token) for token in tokens]
    return stemmed_words


def lem_words(tokens):
    lemmetizer = Lemmatizer()
    stemmed_words = [lemmetizer.lemmatize(token) for token in tokens]
    return stemmed_words


def remove_stop_words(tokens):
    stop_words = get_stopwords()
    filtered_words = [token for token in tokens if token not in stop_words and len(token) > 2]
    return filtered_words


def preprocess_data(contents):
    dataDict = {}
    for content in contents:
        tokens = tokenize_and_remove_punctuations(content['text'])
        filtered_tokens = remove_stop_words(tokens)
        stemmed_tokens = stem_words(filtered_tokens)
        lem_tokens = lem_words(filtered_tokens)
        filtered_tokens1 = remove_stop_words(lem_tokens)
        # dataDict[content['docId']] = lem_tokens
        dataDict[content['docId']] = filtered_tokens1
        # dataDict[content['docId']] = filtered_tokens
        # dataDict[content['docId']] = tokens
        # dataDict[content['docId']] = stemmed_tokens
    return dataDict


def preprocess_queries(input_query):
    queriesDict = {}
    queries = input_query.split('\n')
    i = 1
    for query in queries:
        tokens = tokenize_and_remove_punctuations(query)
        filtered_tokens = remove_stop_words(tokens)
        stemmed_tokens = stem_words(filtered_tokens)
        lem_tokens = lem_words(filtered_tokens)
        filtered_tokens1 = remove_stop_words(lem_tokens)
        queriesDict[i] = filtered_tokens1
        i += 1
    return queriesDict


def get_vocabulary(data):
    tokens = []
    for token_list in data.values():
        tokens = tokens + token_list
    fdist = nltk.FreqDist(tokens)
    return list(fdist.keys())


def generate_inverted_index(data):
    all_words = get_vocabulary(data)
    index = {}
    for word in all_words:
        for doc, tokens in data.items():
            if word in tokens:
                if word in index.keys():
                    index[word].append(doc)
                else:
                    index[word] = [doc]
    return index


def create_inverted_index(data):
    words = {word: [] for word in np.unique(np.concatenate(list(data.values())))}
    dicts_keys = data.keys()
    for key in dicts_keys:
        u_vocab, counts = np.unique(data[key], return_counts=True)
        for i in range(len(u_vocab)):
            words[u_vocab[i]].append({'docID': key, 'frequency': counts[i]})
    od = collections.OrderedDict(sorted(words.items()))
    return od