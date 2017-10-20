#  from gensim import corpora
import random
import pickle
import os
from helpers import get_paragraphs, tokenize

random.seed(123456)


class GenSim:
    def __init__(self):
        cache_path = os.path.join(os.getcwd(), '__cache__')
        self.paragraph_cache = os.path.join(
            cache_path, 'paragraphs.cache')
        self.tokens_cache = os.path.join(cache_path, 'tokens.cache')
        self.book = 'pg3300.txt'
        self.paragraphs = None
        self.tokens = None
        self.load()
        print(len(self.tokens))
        self.save()

    def load(self):
        if os.path.exists(self.paragraph_cache):
            with open(self.paragraph_cache, 'rb') as f:
                self.paragraphs = pickle.load(f)
        else:
            self.paragraphs = get_paragraphs(self.book)

        if os.path.exists(self.tokens_cache):
            with open(self.tokens_cache, 'rb') as f:
                self.tokens = pickle.load(f)
        else:
            self.tokens = tokenize(self.paragraphs)

    def save(self):
        with open(self.paragraph_cache, 'wb') as f:
            pickle.dump(self.paragraphs, f)
        with open(self.tokens_cache, 'wb') as f:
            pickle.dump(self.tokens, f)



gs = GenSim()
#  print(paragraphs[0])
#  tokens = tokenize(paragraphs)
#  print(len(tokens))


#  print(tokens)
#  dictionary = corpora.Dictionary(text)
#  dictionary.save('dict.txt')
#  print(dictionary)
