from helpers import tokenize


class Paragraph:
    def __init__(self, index, paragraph):
        self.index = index
        self.paragraph = paragraph
        self.tokens = None
        self.bag_of_words = None
        self.tokenize()

    def tokenize(self):
        self.tokens = tokenize(self.paragraph)

    def valid(self):
        return self.tokens is not None

    def get_bag(self):
        return self.bag_of_words
