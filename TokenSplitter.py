from Lemmatizer import Lemmatizer


class TokenSplitter():
    def __init__(self):
        self.lemmatizer = Lemmatizer()
        self.lemmatize = self.lemmatizer.lemmatize
        self.words = self.lemmatizer.words

    def split_token_words(self, token):
        candidates = []
        if '‌' in token:
            candidates.append(tuple(token.split('‌')))

        splits = [(token[:s], token[s:]) for s in range(1, len(token)) if token[s - 1] != '‌' and
                  token[s] != '‌'] + [token]
        candidates.extend(list(filter(lambda tokens: set(map(self.lemmatize, tokens)).issubset(self.words), splits)))

        return candidates
