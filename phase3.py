import json
from math import log10
from math import sqrt

file = open('wikipedia.json', 'r')
dictionary = json.load(file)
tf_idf_doc = {}
tf_idf_query = {}
centroids = {}


def calculate_tf(doc, word):
    f = dictionary[word].count(doc)
    tf = 0 if not f else (1 + log10(f))
    return tf


def calculate_idf(word, N=100):
    try:
        df = len(set(dictionary[word]))
    except KeyError:
        return 0
    nt = log10(N / df + 0.01)
    return nt


def calculate_tfidf(N=100):
    words = dictionary.keys()
    number_of_docs = 250
    for doc_index in range(1, number_of_docs + 1):
        for word in words:
            idf = calculate_idf(word, N)
            tf = calculate_tf(doc_index, word)
            if tf and idf:
                try:
                    tf_idf_doc[doc_index].update({word: tf * idf})
                except KeyError:
                    tf_idf_doc[doc_index] = {word: tf * idf}


def calculate_tfidf_queries(search_terms):
    words = list(set(search_terms))
    for word in words:
        idf = calculate_idf(word)
        f = search_terms.count(word)
        tf = 0 if not f else (1 + log10(f))
        if tf and idf:
            tf_idf_query[word] = tf * idf


def calculate_centroids():
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


    return {'Physics': physics_centroid, 'Mathematics': math_centroid, 'Health': health_centroid, 'History': history_centroid,
            'Technology': tech_centroid}


def preprocess_queries(search):
    category = {}
    calculate_tfidf_queries(search)
    for k, v in tf_idf_query.items():
        for ck, vk in centroids.items():
            if vk.get(k, False):
                if category.get(ck, False):
                    category[ck] += (v * vk[k])

                else:
                    category[ck] = (v * vk[k])
    for c in category:
        try:
            category[c] = category[c] / (sqrt(sum(v ** 2 for v in tf_idf_query.values())) * sqrt(
                sum(v ** 2 for v in centroids[c].values())))
        except KeyError:
            pass
    try:
        print('query belongs to:', max(category, key=category.get))
    except ValueError:
        return 'Empty'
    return max(category, key=category.get)


def find_doc_cluster(nearest_cluster):
    doc_score = {}
    categories = ['Physics','Mathematics','Health', 'History', 'Technology']
    if nearest_cluster != 'Empty':
        for c in categories:
            if nearest_cluster == c:
                for n in range((categories.index(c) * 50) + 1, (categories.index(c) * 50) + 51):
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
centroids.update(calculate_centroids())
query = input('Enter your query:\n')
query = query.split()
print(find_doc_cluster(preprocess_queries(query)))
