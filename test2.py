from Normalizer import *
from Stemmer import *
from Lemmatizer import *


class Appearance:

    def __init__(self, docId, frequency):
        self.docId = docId
        self.frequency = frequency

    def __repr__(self):
        return str(self.__dict__)


class Database:

    def __init__(self):
        self.db = dict()

    def __repr__(self):
        return str(self.__dict__)

    def get(self, id):
        return self.db.get(id, None)

    def add(self, document):
        return self.db.update({document['id']: document})

    def remove(self, document):
        return self.db.pop(document['id'], None)


single_chars = ['»', '.', '«', '،', '؟', '"', '#', ')', '(', '*', ',', '-', '/', ':', '[', ']', '،', '?', '…', '۰',
                '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '-', '+', '=', '@', '$', '$', '%', '^', '&', '-', '_',
                '{', '}', '\'', '/', ';', '  ', '>', '<', '•', '٪', '؛']


class InvertedIndex:

    def __init__(self, db):
        self.index = dict()
        self.db = db

    def __repr__(self):
        return str(self.index)

    def index_document(self, document):
        single_chars = ['»', '.', '«', '،', '؟', '"', '#', ')', '(', '*', ',', '-', '/', ':', '[', ']', '،', '?', '…',
                        '۰',
                        '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '-', '+', '=', '@', '$', '$', '%', '^', '&', '-',
                        '_',
                        '{', '}', '\'', '/', ';', '  ', '>', '<', '•', '٪', '؛']
        text = document['text'].strip(u'\xa0\u200c \t\n\r\f\v')
        text = text.replace('\n', ' ')
        text = Normalizer().normalize(text)
        for sc in single_chars:
            if text.__contains__(sc):
                text = text.replace(sc, ' ')
        terms = text.split(' ')
        appearances_dict = dict()

        for term in terms:
            if term.__eq__(''):
                terms.remove(term)
            if term.isnumeric():
                terms.remove(term)
            term_frequency = appearances_dict[term].frequency if term in appearances_dict else 0
            appearances_dict[term] = Appearance(document['id'], term_frequency + 1)

        update_dict = {key: [appearance]
        if key not in self.index
        else self.index[key] + [appearance]
                       for (key, appearance) in appearances_dict.items()}
        self.index.update(update_dict)

        self.db.add(document)
        return document

    def lookup_query(self, query):
        lem = Lemmatizer()
        stem = Stemmer()
        return {term: self.index[term] for term in query.split(' ') if term in self.index}


def highlight_term(id, term, text):
    replaced_text = text.replace(term, "\033[1;32;40m {term} \033[0;0m".format(term=term))
    return "--- document {id}: {replaced}".format(id=str(id).split("docs/")[1], replaced=replaced_text)


db = Database()
index = InvertedIndex(db)

docs = []
for i in range(1, 100):
    file = open("docs/" + str(i) + ".txt", "r", encoding='utf8')
    docs.append({
        'id': file.name.split('.txt')[0],
        'text': file.read()
    })
# print(docs)
for i in range(len(docs)):
    index.index_document(docs[i])

search_term = input('جست و جو کنید: ')
result = index.lookup_query(search_term)

sum = 0
for term in result.keys():
    for appearance in result[term]:
        document = db.get(appearance.docId)
        print(highlight_term(appearance.docId, term, document['text']))
        print("frequency = ", appearance.frequency)
        sum += appearance.frequency
        print("-----------------------------")
# print(result)
for res in result.items():
    print(res)
print(sum)
