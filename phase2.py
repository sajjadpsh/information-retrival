import os
import nltk
from Stemmer import *
from Lemmatizer import *
from Normalizer import *
import math
import operator
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
    # print(text)
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
    queries = input_query.split(' ')
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


# def create_inverted_index(data):
#     words = {word: [] for word in np.unique(np.concatenate(list(data.values())))}
#     dicts_keys = data.keys()
#     for key in dicts_keys:
#         u_vocab, counts = np.unique(data[key], return_counts=True)
#         for i in range(len(u_vocab)):
#             words[u_vocab[i]].append({'docID': key, 'frequency': counts[i]})
#     od = collections.OrderedDict(sorted(words.items()))
#     return od


def calculate_tf(tokens):
    tf_score = {}
    for token in tokens:
        tf_score[token] = tokens.count(token)
    return tf_score


def calculate_idf(data):
    idf_score = {}
    N = len(data)
    all_words = get_vocabulary(data)
    for word in all_words:
        word_count = 0
        for token_list in data.values():
            if word in token_list:
                word_count += 1
        idf_score[word] = math.log10(N / word_count)
    return idf_score


def calculate_tfidf(data, idf_score):
    scores = {}
    for key, value in data.items():
        scores[key] = calculate_tf(value)
    for doc, tf_scores in scores.items():
        for token, score in tf_scores.items():
            tf = score
            idf = idf_score[token]
            tf_scores[token] = (1 + math.log10(tf)) * idf
    return scores


def calculate_tfidf_queries(queries, idf_score):
    scores = {}
    for key, value in queries.items():
        scores[key] = calculate_tf(value)
    for key, tf_scores in scores.items():
        for token, score in tf_scores.items():
            idf = 0
            tf = score
            if token in idf_score.keys():
                idf = idf_score[token]
            tf_scores[token] = (1 + math.log10(tf)) * idf
    return scores
lemmatizer = Lemmatizer()
normalizer = Normalizer()
print(normalizer.normalize('می روم'))
print(lemmatizer.lemmatize(normalizer.normalize("می روم")))
# stemmer = Stemmer()
# print(stemmer.stem(normalizer.normalize("رفته بودم")))
# data = read_data("docs")
# preprocessed_data = preprocess_data(data)
#
# inverted_index = generate_inverted_index(preprocessed_data)
# print(inverted_index)
# # inverted_index = create_inverted_index(preprocessed_data)
# query = "لیگ قهرمانان آسیا"
# queries = preprocess_queries(query)
# print(inverted_index)
# idf_scores = calculate_idf(preprocessed_data)
# data_scores = calculate_tfidf(preprocessed_data, idf_scores)
# query_scores = calculate_tfidf_queries(queries, idf_scores)
# # print(query_scores)
# # print(data_scores)
#
#
# query_docs = {}
# for key, value in queries.items():
#     doc_sim = {}
#     for term in value:
#         if term in inverted_index.keys():
#             docs = inverted_index[term]
#             # print(docs)
#             for doc in docs:
#                 doc_score = data_scores[doc][term]
#                 doc_length = math.sqrt(sum(x ** 2 for x in data_scores[doc].values()))
#                 query_score = query_scores[key][term]
#                 query_length = math.sqrt(sum(x ** 2 for x in query_scores[key].values()))
#                 cosine_sim = (doc_score * query_score) / (doc_length * query_length)
#                 if doc in doc_sim.keys():
#                     doc_sim[doc] += cosine_sim
#                 else:
#                     doc_sim[doc] = cosine_sim
#     ranked = sorted(doc_sim.items(), key=operator.itemgetter(1), reverse=True)
    # print(ranked)
    # ranked = heap_sort(doc_sim.items())
    # print(ranked)
    # query_docs[key] = ranked

# print(query_docs)
