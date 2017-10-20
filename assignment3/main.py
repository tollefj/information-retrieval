from _gensim import GenSim

if __name__ == '__main__':
    gs = GenSim()
    gs.read_stopwords()
    gs.load()
    gs.build_dictionary()
    gs.build_bag()
    gs.build_tfidf_model()
    gs.build_lsi_model()
