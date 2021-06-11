import math
from collections import Counter, OrderedDict
from typing import List, Dict
from functools import reduce


def compute_tf(corpus: List[List[str]]) -> Dict[str, float]:
    tf_dict = Counter(reduce(lambda a, b: a + b, corpus))
    for word in tf_dict:
        tf_dict[word] /= len(tf_dict)

    return tf_dict


def compute_idf(word: str, corpus: List[List[str]]) -> float:
    return math.log10(len(corpus) / sum([1 for text in corpus if word in text]))


def compute_tfidf(corpus: List[List[str]]) -> Dict[str, float]:
    tfidf_dict = compute_tf(corpus)
    for word in tfidf_dict:
        tfidf_dict[word] *= compute_idf(word, corpus)
    return sort_dict(tfidf_dict)


def sort_dict(dictionary: Dict[str, float]) -> Dict[str, float]:
    sorted_pairs = [(k, dictionary[k]) for k in sorted(dictionary, key=dictionary.get, reverse=True)]
    sorted_dict = OrderedDict(sorted_pairs)
    for word in sorted_dict:
        sorted_dict[word] = round(sorted_dict[word], 4)
    return sorted_dict
