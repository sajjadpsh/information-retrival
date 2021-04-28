from nltk.stem.api import StemmerI


class Stemmer(StemmerI):

    def __init__(self):
        self.ends = ['ات', 'ان', 'ترین', 'تر', 'م', 'ت', 'ش', 'یی', 'ی', 'ها', 'ٔ', '‌ا', '‌']

    def stem(self, word):
        for end in self.ends:
            if word.endswith(end):
                word = word[:-len(end)]

        if word.endswith('ۀ'):
            word = word[:-1] + 'ه'

        return word
