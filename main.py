# import BM25
from BM25 import entry
import Scoring

if __name__ == '__main__':
    length_BM25 = 5
    path_Query = './data/10_query_list.txt'
    path_Corpus = './data/1K_scotus_corpus.txt'
    # path_Corpus = './data/all_scotus_corpus.txt'
    # path_Corpus = './data/test_scotus_corpus.txt'

    entry.main_BM25(path_Query, path_Corpus, length_BM25)