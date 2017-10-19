import codecs
import re
from stemming import stem_word


def get_paragraphs(file_name):
    paragraphs = None
    with codecs.open(file_name, 'r', 'utf-8') as book:
        paragraphs = book.read().split('\r\n\r\n')
    return paragraphs


def keep_alnum(s):
    return re.sub('[^A-Za-z0-9\\s]+', '', s.lower())


def tokenize(paragraphs):
    tokens = list()
    for paragraph in paragraphs:
        p = keep_alnum(paragraph).split()
        valid = True
        for w in p:
            if 'gutenberg' in w:
                valid = False
        if valid:
            # fetch stemmed words from a memoized stemming function
            tokens.append([stem_word(w) for w in p])
    return tokens
