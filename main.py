import random
from gensim import corpora, models
from helpers import get_paragraphs, tokenize

random.seed(123456)


class Paragraph:
    def __init__(self, index, paragraph):
        #  print('New paragraph ' + str(index))
        self.index = index
        self.paragraph = paragraph

        self.tokens = None
        self.bag_of_words = None

        self.tokenize()

    def tokenize(self):
        self.tokens = tokenize(self.paragraph)

    def build_bag_of_words(self, stopwords):
        d = corpora.Dictionary([self.tokens])
        stop_ids = [d.token2id[sw] for sw in stopwords
                    if sw in d.token2id]
        d.filter_tokens(stop_ids)
        self.bag_of_words = d.doc2bow(self.tokens)
        #  print(self.bag_of_words)

    def valid(self):
        return self.tokens is not None

    def get_bag(self):
        return self.bag_of_words


class GenSim:
    def __init__(self):
        self.book = 'pg3300.txt'
        self.stopwords = None

        self.corpus = []  # paragraph class
        self.tfidf_corpus = None
        self.lsi_corpus = None
        self.dictionary = []
        self.bag = []

        self.read_stopwords()
        self.load()
        self.build_tfidf_model()
        self.build_lsi_model()

    def read_stopwords(self):
        with open('stopwords.txt', 'r') as f:
            self.stopwords = f.read().split(',')

    def load(self):
        all_tokens = []
        for i, p in enumerate(get_paragraphs(self.book)):
            paragraph = Paragraph(i, p)
            if paragraph.valid():
                paragraph.build_bag_of_words(self.stopwords)
                all_tokens.append(paragraph.tokens)
                self.bag.append(paragraph.bag_of_words)
                self.corpus.append(paragraph)
        self.dictionary = corpora.Dictionary(all_tokens)

    def build_tfidf_model(self):
        tfidf_model = models.TfidfModel(self.bag)
        self.tfidf_corpus = tfidf_model[self.bag]
        print(tfidf_model)

    def build_lsi_model(self):
        print(self.dictionary)
        lsi = models.LsiModel(self.tfidf_corpus,
                              id2word=self.dictionary, num_topics=100)
        print(lsi)


gs = GenSim()
