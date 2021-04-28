import re
from Lemmatizer import Lemmatizer
from WordTokenizer import WordTokenizer
from words import maketrans

compile_patterns = lambda patterns: [(re.compile(pattern), repl) for pattern, repl in patterns]


class Normalizer(object):
    def __init__(self, remove_extra_spaces=True, persian_style=True, persian_numbers=True, remove_diacritics=True,
                 affix_spacing=True, token_based=False, punctuation_spacing=True):
        self._punctuation_spacing = punctuation_spacing
        self._affix_spacing = affix_spacing
        self._token_based = token_based

        translation_src, translation_dst = ' ىكي“”', ' یکی""'
        if persian_numbers:
            translation_src += '0123456789%'
            translation_dst += '۰۱۲۳۴۵۶۷۸۹٪'
        self.translations = maketrans(translation_src, translation_dst)

        if self._token_based:
            lemmatizer = Lemmatizer()
            self.words = lemmatizer.words
            self.verbs = lemmatizer.verbs
            self.tokenizer = WordTokenizer(join_verb_parts=False)
            self.suffixes = {'ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش'}

        self.character_refinement_patterns = []

        if remove_extra_spaces:
            self.character_refinement_patterns.extend([
                (r' +', ' '),
                (r'\n\n+', '\n\n'),
                (r'[ـ\r]', ''),
            ])

        if persian_style:
            self.character_refinement_patterns.extend([
                ('"([^\n"]+)"', r'«\1»'), ('([\d+])\.([\d+])', r'\1٫\2'),
                (r' ?\.\.\.', ' …'),
            ])

        if remove_diacritics:
            self.character_refinement_patterns.append(
                ('[\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652]', ''),
            )

        self.character_refinement_patterns = compile_patterns(self.character_refinement_patterns)

        punc_after, punc_before = r'\.:!،؛؟»\]\)\}', r'«\[\(\{'
        if punctuation_spacing:
            self.punctuation_spacing_patterns = compile_patterns([
                ('" ([^\n"]+) "', r'"\1"'),
                (' ([' + punc_after + '])', r'\1'),
                ('([' + punc_before + ']) ', r'\1'),
                ('([' + punc_after[:3] + '])([^ ' + punc_after + '\d۰۱۲۳۴۵۶۷۸۹])', r'\1 \2'),
                ('([' + punc_after[3:] + '])([^ ' + punc_after + '])', r'\1 \2'),
                ('([^ ' + punc_before + '])([' + punc_before + '])', r'\1 \2'),
            ])

        if affix_spacing:
            self.affix_spacing_patterns = compile_patterns([
                (r'([^ ]ه) ی ', r'\1‌ی '),
                (r'(^| )(ن?می) ', r'\1\2‌'),
                (
                    r'(?<=[^\n\d ' + punc_after + punc_before + ']{2}) (تر(ین?)?|گری?|های?)(?=[ \n' +
                    punc_after + punc_before + ']|$)', r'‌\1'),
                (r'([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n' + punc_after + ']|$)', r'\1‌\2'),
            ])

    def normalize(self, text):
        text = self.character_refinement(text)
        if self._affix_spacing:
            text = self.affix_spacing(text)

        if self._token_based:
            tokens = self.tokenizer.tokenize(text.translate(self.translations))
            text = ' '.join(self.token_spacing(tokens))

        if self._punctuation_spacing:
            text = self.punctuation_spacing(text)

        return text

    def character_refinement(self, text):

        text = text.translate(self.translations)
        for pattern, repl in self.character_refinement_patterns:
            text = pattern.sub(repl, text)
        return text

    def punctuation_spacing(self, text):

        for pattern, repl in self.punctuation_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def affix_spacing(self, text):

        for pattern, repl in self.affix_spacing_patterns:
            text = pattern.sub(repl, text)
        return text

    def token_spacing(self, tokens):

        result = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + '‌' + token
                if token_pair in self.verbs or token_pair in self.words and self.words[token_pair][0] > 0:
                    joined = True

                    if t < len(tokens) - 1 and token + '_' + tokens[t + 1] in self.verbs:
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result
