import datetime
import json
import math
from math import log10
from math import sqrt

file = open('wikipedia.json')
dictionary = json.load(file)
tf_idf_doc = {}
tf_idf_query = {}
centroids = {}
# dictionary = {}
categories = ['Health', 'History', 'Mathematics', 'Physics', 'Technology']
a = datetime.datetime.now()
# for category in categories:
#     mypath = "IR" + '/' + category
#     file = read_data(mypath)
#     pre = preprocess_data(file)
#     inverted_index = generate_inverted_index(pre)
#     dictionary[category] = inverted_index
b = datetime.datetime.now()
print((b - a).seconds, ',', (b - a).microseconds)


def compute_tf(doc, word):
    f = dictionary[word].count(doc)
    tf = 0 if not f else (1 + log10(f))
    return tf


def compute_idf(word):
    try:
        df = len(set(dictionary[word]))
    except KeyError:
        return 0
    nt = log10(100 / df + 0.01)
    return nt


def calculate_tfidf():
    words = dictionary.keys()
    # words = champ_list.keys()
    number_of_docs = 250
    for doc_index in range(1, number_of_docs + 1):
        for word in words:
            idf = compute_idf(word)
            tf = compute_tf(doc_index, word)
            if tf and idf:
                try:
                    tf_idf_doc[doc_index].update({word: tf * idf})
                except KeyError:
                    tf_idf_doc[doc_index] = {word: tf * idf}


def compute_tf_idf_query(search_terms):
    words = list(set(search_terms))
    for word in words:
        idf = compute_idf(word)
        f = search_terms.count(word)
        tf = 0 if not f else (1 + log10(f))
        if tf and idf:
            tf_idf_query[word] = tf * idf


def compute_cluster_centroid():
    physics_words, math_words, health_words, tech_words, history_words = [], [], [], [], []
    physics_centroid, math_centroid, health_centroid, tech_centroid, history_centroid = {}, {}, {}, {}, {}

    for doc_index in range(1, 51):
        physics_words.extend(list(tf_idf_doc[doc_index].keys()))
    for doc_index in range(51, 101):
        math_words.extend(list(tf_idf_doc[doc_index].keys()))
    for doc_index in range(101, 151):
        health_words.extend(list(tf_idf_doc[doc_index].keys()))
    for doc_index in range(151, 201):
        history_words.extend(list(tf_idf_doc[doc_index].keys()))
    for doc_index in range(201, 251):
        tech_words.extend(list(tf_idf_doc[doc_index].keys()))

    physics_words, math_words, health_words, tech_words, history_words = list(set(physics_words)), list(
        set(math_words)), list(set(health_words)), list(
        set(tech_words)), list(set(history_words))

    for word in physics_words:
        physics_centroid[word] = 0
        for n in range(1, 51):
            if tf_idf_doc[n].get(word, False):
                physics_centroid[word] += tf_idf_doc[n][word] / 50

    for word in math_words:
        math_centroid[word] = 0
        for n in range(51, 101):
            if tf_idf_doc[n].get(word, False):
                math_centroid[word] += tf_idf_doc[n][word] / 50

    for word in health_words:
        health_centroid[word] = 0
        for n in range(101, 151):
            if tf_idf_doc[n].get(word, False):
                health_centroid[word] += tf_idf_doc[n][word] / 50

    for word in history_words:
        history_centroid[word] = 0
        for n in range(151, 201):
            if tf_idf_doc[n].get(word, False):
                history_centroid[word] += tf_idf_doc[n][word] / 50

    for word in tech_words:
        tech_centroid[word] = 0
        for n in range(201, 251):
            if tf_idf_doc[n].get(word, False):
                tech_centroid[word] += tf_idf_doc[n][word] / 50

    return {'physics': physics_centroid, 'math': math_centroid, 'health': health_centroid, 'history': history_centroid,
            'tech': tech_centroid}


def user_query(search):
    clusters = {}
    compute_tf_idf_query(search)
    for k, v in tf_idf_query.items():
        for ck, vk in centroids.items():
            if vk.get(k, False):
                if clusters.get(ck, False):
                    clusters[ck] += (v * vk[k])

                else:
                    clusters[ck] = (v * vk[k])
    for c in clusters:
        try:
            clusters[c] = clusters[c] / (sqrt(sum(v ** 2 for v in tf_idf_query.values())) * sqrt(
                sum(v ** 2 for v in centroids[c].values())))
        except KeyError:
            pass
    try:
        print(f'query is closer to the centroid of -> {max(clusters, key=clusters.get)}')
    except ValueError:
        return 'Empty'
    # return clusters
    return max(clusters, key=clusters.get)


def find_nearest_documents(nearest_cluster):
    doc_score = {}
    clusters = ['physics', 'math', 'health', 'history', 'tech']
    if nearest_cluster != 'Empty':
        for c in clusters:
            if nearest_cluster == c:
                for n in range((clusters.index(c) * 50) + 1, (clusters.index(c) * 50) + 51):
                    for k, v in tf_idf_query.items():
                        if tf_idf_doc[n].get(k, False):
                            if doc_score.get(n, False):
                                doc_score[n] += (v * tf_idf_doc[n][k])
                            else:
                                doc_score[n] = (v * tf_idf_doc[n][k])
        for c in doc_score:
            doc_score[c] = doc_score[c] / (sqrt(sum(v ** 2 for v in tf_idf_query.values())) * sqrt(
                sum(v ** 2 for v in tf_idf_doc[c].values())))

        return {k: v for k, v in sorted(doc_score.items(), key=lambda item: item[1], reverse=True)}
    else:
        return "No documents found"


calculate_tfidf()
compute_cluster_centroid()
search_terms = "سلامتی"
search_terms = search_terms.split()
print(find_nearest_documents(user_query(search_terms)))
print()
