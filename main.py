import re
import time
import gensim

# import BM25
# import Scoring
from BM25 import entry
from Scoring import wordLevel_QC_relatedness

if __name__ == '__main__':
    length_BM25 = 5
    path_Query = './data/10_query_list.txt'
    path_Corpus = './data/1K_scotus_corpus.txt'
    # path_Corpus = './data/all_scotus_corpus.txt'
    # path_Corpus = './data/test_scotus_corpus.txt'

    queries, dict_BM25 = entry.main_BM25(path_Query, path_Corpus, length_BM25)
    print(queries)
    print(dict_BM25)

    # here we load word2vec model to save loading time. Will be change in the future.
    pretrained_embedding_path = "../word2vec/GoogleNews-vectors-negative300.bin"
    tic = time.time()
    print('Please wait ... (it could take a while to load the file : {})'.format(pretrained_embedding_path))
    model = gensim.models.KeyedVectors.load_word2vec_format(pretrained_embedding_path, binary=True)
    print('Done.  (time used: {:.1f}s)\n'.format(time.time()-tic))
    # embedding_dim = 300


    corpus_dir = './data/all_scotus_text/'
    # for i in range(len(queries)):
    for i in range(1):
        each_query_result_list = dict_BM25.get(i, 0)
        print(each_query_result_list) # docs ID
        embedding_each_query = wordLevel_QC_relatedness.get_embeddings_from_pretrained_googlenews_w2v(queries[i], model)
        print('length of query embedding: ', len(embedding_each_query))

        for j in range(len(each_query_result_list)):
            file_name = corpus_dir + str(each_query_result_list[j]) + '.txt'
            with open(file_name, 'r') as f:
                each_doc_text = f.read().lower().split()
                # if j ==0:
                embedding_each_doc = wordLevel_QC_relatedness.get_embeddings_from_pretrained_googlenews_w2v(each_doc_text, model)
                print('length of doc embedding: ', len(embedding_each_doc))
                score = wordLevel_QC_relatedness.calc_wordLevel_QC_relatedness_score(embedding_each_query, embedding_each_doc)
                print('score: ', score)
                print()
                    # print(each_doc_text)
                # print('length of each doc text: ', len(each_doc_text))




                # tmp = []
                # for line in f.readlines():
                #     line = line.lower()
                #     # desc = line.strip().split('\t')
                #     # item = line.split()
                #     item = re.split('\W', line)
                #     tmp.extend(item)
                # print('tmp: ', len(tmp))





