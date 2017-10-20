from gensim import corpora, models, similarities
from helpers import get_paragraphs, tokenize
from _paragraph import Paragraph


class GenSim:
    def __init__(self):
        self.book = 'pg3300.txt'
        self.stopwords = None
        self.corpus = list()            # paragraph tokens
        self.orig_paragraphs = list()   # unchanged paragraph
        self.bag = list()               # list of doc2bow for all paragraphs
        self.dictionary = None          # gensim dictionary

        self.tfidf_model = None
        self.tfidf_corpus = None
        self.lsi_model = None
        self.lsi_corpus = None
        self.bag = list()

        self.read_stopwords()
        self.load()
        self.build_dictionary()
        self.build_bag()
        self.build_tfidf_model()
        self.build_lsi_model()
        # runs both tf and lsi models
        self.query("How taxes influence Economics?")

    def read_stopwords(self):
        with open('stopwords.txt', 'r') as f:
            self.stopwords = f.read().split(',')

    def load(self):
        for i, p in enumerate(get_paragraphs(self.book)):
            paragraph = Paragraph(i, p)
            if paragraph.valid():
                # append the tokenized paragraph to corpus
                self.corpus.append(paragraph.tokens)
                # store the original paragraphs
                self.orig_paragraphs.append(p)

    def build_dictionary(self):
        d = corpora.Dictionary(self.corpus)
        stop_ids = [d.token2id[sw] for sw in self.stopwords
                    if sw in d.token2id]
        d.filter_tokens(stop_ids)
        self.dictionary = d

    def build_bag(self):
        for p in self.corpus:
            self.bag.append(self.dictionary.doc2bow(p))

    def build_tfidf_model(self):
        self.tfidf_model = models.TfidfModel(self.bag)
        self.tfidf_corpus = self.tfidf_model[self.bag]
        self.tfidf_index = similarities.MatrixSimilarity(self.tfidf_corpus)

    def build_lsi_model(self):
        self.lsi_model = models.LsiModel(self.tfidf_corpus,
                                         id2word=self.dictionary,
                                         num_topics=100)
        self.lsi_corpus = self.lsi_model[self.tfidf_corpus]
        self.lsi_index = similarities.MatrixSimilarity(self.lsi_corpus)

    def similarity(self, model, index, query):
        def preprocess(query):
            query = tokenize(query)
            return self.dictionary.doc2bow(query)
        query = model[preprocess(query)]
        doc2similarity = enumerate(index[query])
        indexes = sorted(doc2similarity, key=lambda x: -x[1])[:3]
        for index in indexes:
            print(self.orig_paragraphs[index[0]])
            print()
        return query  # returns the processed query

    def sim_tf(self, query):
        self.similarity(self.tfidf_model, self.tfidf_index, query)

    def sim_lsi(self, query):
        def show_topics(topics):
            print("The top 3 topics are:\n")
            for topic in enumerate(topics):
                t = topic[1][0]
                print(self.lsi_model.show_topics()[t])
            print()
        model_query = self.similarity(self.lsi_model, self.lsi_index, query)
        topics = sorted(model_query, key=lambda kv: -abs(kv[1]))[:3]
        show_topics(topics)

    def query(self, q):
        self.sim_tf(q)
        self.sim_lsi(q)
