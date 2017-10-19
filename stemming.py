from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()

# init a memoize class for using as a decorator
# for simple look-up functions as stemming
# stores each result from a function
# in cache for quick look-up


def memoize(func):
    class memo(dict):
        __slots__ = ()

        def __missing__(self, key):
            self[key] = val = func(key)
            return val
    return memo().__getitem__


@memoize
def stem_word(w):
    return stemmer.stem(w)
