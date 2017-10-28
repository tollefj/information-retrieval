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


def idf(Nt):
    N = len(docs)
    return math.log((N / Nt), 2)


def tf(doc, term):
    return doc.count(term)


def get_avg_doc_len():
    total_len = 0
    for doc in docs:
        tmp_len = len(doc[1].split())
        total_len += tmp_len
    return float(total_len / len(docs))


bm25_q1 = dict()
bm25_q2 = dict()
avgdl = get_avg_doc_len()
_k = 1.2
_b = 0.75
q1 = "Trump President"
q2 = "Hillary"
queries = [q1, q2]

for doc in docs:
    for Q in queries:
        query_score = 0
        #  print("on query: " + Q)
        for qi in Q.split(' '):
            #  print("On term " + qi)
            _IDF = idf(get_nt(qi))

            fqiD = tf(doc[1], qi)
            print(doc[1])
            print(len(doc[1]))
            D = len(doc[1].split())
            tmp_score = _IDF * ((fqiD * (_k + 1)) /
                                (fqiD + _k * (1 - _b + (_b * (D / avgdl)))))
            query_score += tmp_score
        if q2 in Q:
            bm25_q2["Doc " + str(doc[0]) + " " + doc[1] + ", Q: " + Q] = query_score
        else:
            bm25_q1["Doc " + str(doc[0]) + " " + doc[1] + ", Q: " + Q] = query_score
for k, v in reversed(sorted(bm25_q1.items(), key=lambda x: x[1])):
    print(k, v)
for k, v in reversed(sorted(bm25_q2.items(), key=lambda x: x[1])):
    print(k, v)
