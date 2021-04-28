import tokenize
from hazm import *
import re

class Tokenizer():
    def __init__(self):
        pass

    def tokenize_words(self, doc_string):
        token_list = doc_string.strip().split()
        token_list = [x.strip("\u200c") for x in token_list if len(x.strip("\u200c")) != 0]
        return token_list

    def add_tab(self, mystring):
        mystring = mystring.group()  # this method return the string matched by re
        mystring = mystring.strip(' ')  # ommiting the whitespace around the pucntuation
        mystring = mystring.strip('\n')  # ommiting the newline around the pucntuation
        mystring = " " + mystring + "\t\t"  # adding a space after and before punctuation
        return mystring


single_chars = ['»', '.', '«', '،', '؟', '"', '#', ')', '(', '*', ',', '-', '/', ':', '[', ']', '،', '?', '…', '۰',
                '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹', '-', '+', '=', '@', '$', '$', '%', '^', '&', '-', '_',
                '{', '}', '\'', '/', ';', '  ', '>', '<', '•', '٪', '؛']
persian_alphabet = ["ا", "ب", "پ", "ت", "ث", "ج", "چ", "ح", "خ", "د", "ذ", "ر", "ز", "ژ", "س", "ش", "ص", "ض", "ط",
                    "ظ",
                    "ع", "غ", "ف", "ق",
                    "ک", "گ", "ل", "م", "ن", "و", "ه", "ی"]
file = open("1.txt", "r", encoding='utf8')
lines = file.readlines()
text = ''
for line in lines:
    for c in line:
        text += c
text = text.strip(u'\xa0\u200c \t\n\r\f\v')
text = text.replace('\n', ' ')
for sc in single_chars:
    if text.__contains__(sc):
        text = text.replace(sc, ' ')
words1 = text.split(' ')
print(words1)
print(len(words1))
for word in words1:
    if word.__eq__(''):
        words1.remove(word)
    if word.isnumeric():
        words1.remove(word)
    for sc in single_chars:
        if word.__contains__(sc):
            words1.remove(word)
    for pa in persian_alphabet:
        if word.__eq__(pa):
            words1.remove(word)
print(words1)
print(len(words1))
