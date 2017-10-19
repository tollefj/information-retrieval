#  from gensim import corpora
import random
from helpers import get_paragraphs, tokenize

random.seed(123456)


paragraphs = get_paragraphs('pg3300.txt')
tokens = tokenize(paragraphs)
print(len(tokens))


#  print(tokens)
#  dictionary = corpora.Dictionary(text)
#  dictionary.save('dict.txt')
#  print(dictionary)
