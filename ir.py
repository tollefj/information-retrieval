import math
from collections import OrderedDict


docs = OrderedDict({
    1: 'Trump Hillary Trump Trump',
    2: 'President Hillary Hillary',
    3: 'Trump Hillary Hillary',
    4: 'President Trump',
    5: 'Hillary',
    6: 'President President',
    7: 'Hillary Hillary President Trump President Hillary Trump',
    8: 'President',
    9: 'President Hillary Trump',
    10: 'President Trump Trump President'
})
docs = sorted(docs.items())


''' Task 1.1.1 - TF and IDF '''


def tf(doc, term):
    return doc.count(term)


def print_tf():
    for doc in docs:
        docnum = str(doc[0])
        d = doc[1]
        print(docnum + " P: " + str(tf(d, "President")) +
              " T: " + str(tf(d, "Trump")) +
              " H: " + str(tf(d, "Hillary")))


print("TASK 1.1.3")
print_tf()


def idf(Nt):
    N = len(docs)
    return math.log((N / Nt), 2)


def num_of_docs_where_term_appears(term):
    occurrences = 0
    for doc_num, sentence in docs:
        if term in sentence:
            occurrences += 1
    print(term + " appeared " + str(occurrences) + " times in all documents")
    return float(occurrences)


trump_Nt = num_of_docs_where_term_appears("Trump")
hillary_Nt = num_of_docs_where_term_appears("Hillary")
pres_Nt = num_of_docs_where_term_appears("President")


def get_nt(term):
    if "Pres" in term:
        return pres_Nt
    elif "Hil" in term:
        return hillary_Nt
    elif "Tru" in term:
        return trump_Nt


''' Task 1.1.4 '''


def tfidf():
    # high weight tf-idf: high term frequency and a low doc frequency
    # weighting scheme: (1 + log2(tf(t,d)) * log2(N/dft))
    compare_doc = docs[5]
    for t in compare_doc[1].split():
        comp_idf = idf(get_nt(t))
        comp_tf = tf(compare_doc[1], t)
        comp_tfidf = round(comp_idf * comp_tf, 5)
        print(comp_tfidf)
    for doc in [docs[i - 1] for i in [2, 4, 8, 9]]:
        print("Handling doc " + str(doc[0]))
        for t in doc[1].split():
            _idf = idf(get_nt(t))
            _tf = tf(doc[1], t)
            _tfidf = round(_idf * _tf, 5)
            print(t + ": " + str(_tfidf))


print("TASK 1.1.4")
tfidf()
# Eucl. distance calculated manually.


''' Task 1.1.5 '''


def cos_sim():
    print("Calculating cosine similarity")
    q5 = "President"
    cos_sim_sorted = dict()
    for doc in docs:
        print("Document " + str(doc[0]))
        # calc dot product
        # divide by vector length of term vs query
        doc_dict = OrderedDict()
        query_dict = OrderedDict()
        for term in doc[1].split():
            doc_dict[term] = doc[1].count(term)
            query_dict[term] = 1 if term == q5 else 0
        #  doc_dict = dict(doc_dict)
        #  query_dict = dict(query_dict)
        print(dict(doc_dict))
        _d = list(doc_dict.values())
        _q = list(query_dict.values())
        print(_d)
        print(_q)

        dot_prod = 0
        d_squared = 0
        q_squared = 0
        for i in range(len(doc_dict)):
            dot_prod += (_d[i] * _q[i])
            d_squared += _d[i]**2
            q_squared += _q[i]**2
        d_vec_length = math.sqrt(d_squared)
        q_vec_length = math.sqrt(q_squared)
        #  print(dot_prod)
        #  print(d_vec_length)
        #  print(q_vec_length)
        try:
            doc_cos_sim = dot_prod / (d_vec_length * q_vec_length)
        except ZeroDivisionError:
            doc_cos_sim = 0
        print("Cos.sim for doc " + str(doc[0]) + " = " + str(doc_cos_sim))
        cos_sim_sorted[doc[0]] = doc_cos_sim
    for score in reversed(sorted(cos_sim_sorted.items(), key=lambda x: x[1])):
        print("Doc " + str(score[0]) + ": " + str(round(score[1], 5)))


print("TASK 1.1.5")
cos_sim()
