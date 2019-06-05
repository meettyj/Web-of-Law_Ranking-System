import re
import time
import gensim
from rake_nltk import Rake
import numpy as np

# import BM25
# import Scoring
from BM25 import entry
from Scoring import wordLevel_QC_relatedness
from Scoring import dateExtractor
from Scoring import normalization
from Scoring import citation
from Scoring import paragraph_citation

# ------------------------------------------------------------------------------------
# from main method
length_BM25 = 20
path_Query = './data/10_query_list.txt'
path_Corpus = './data/1K_scotus_corpus.txt'
# path_Corpus = './data/all_scotus_corpus.txt'
# path_Corpus = './data/test_scotus_corpus.txt'

queries, dict_BM25, dict_BM25_with_score = entry.main_BM25(path_Query, path_Corpus, length_BM25)
print('queries: ', queries)
print()
print('dictionary for result after BM25: ', dict_BM25)
print()

# here we load word2vec model to save loading time. Will be change in the future.
# pretrained_embedding_path = "../word2vec/GoogleNews-vectors-negative300.bin"
# tic = time.time()
# print('Please wait ... (it could take a while to load the file : {})'.format(pretrained_embedding_path))
# model = gensim.models.KeyedVectors.load_word2vec_format(pretrained_embedding_path, binary=True)
# print('Done.  (time used: {:.1f}s)\n'.format(time.time() - tic))
# embedding_dim = 300

# initialize for Key Phrases Overlap (second part of Scoring)
rake_object = Rake()

corpus_dir = './data/all_scotus_text/'
date_dir = './data/all_scotus_NYU_IE1/'

# Paragraph citation part



for i in range(len(queries)):
    # for i in range(1): # for development setting
    print('============================== Query{}: {} =================================='.format(i + 1, queries[i]))
    # BM25 score weight list
    # print('dict_BM25_with_score: ', dict_BM25_with_score)
    # print(dict_BM25_with_score[i])
    # normalized_BM25_weight_list = normalization.normalize_list(dict_BM25_with_score[i])
    # print('BM25 weight list: ', normalized_BM25_weight_list)
    # print()
    each_query_result_list = dict_BM25.get(i, 0)
    print('each_query_result_list: ', each_query_result_list)
    simple_final_score_dict = {}


    # Paragraph citation part
    citation_dir = './data/citation/'
    specific_citation_dir = './data/all_scotus_NYU_IE1/'
    text_dir = './data/all_scotus_text/'
    citation_graph = citation.get_citation_graph(citation_dir)
    docID2citeID, citeID2docID = citation.get_docID2citeID_and_citeID2docID(citation_dir)

    in_degree_citation_weight_paragraph = [(str(item), 0.1) for item in each_query_result_list]
    out_degree_citation_weight_paragraph = [(str(item), 0.1) for item in each_query_result_list]
    in_degree_citation_weight_dict_paragraph = dict(in_degree_citation_weight_paragraph)
    out_degree_citation_weight_dict_paragraph = dict(out_degree_citation_weight_paragraph)

    # ever_met_file_list = []
    for j in range(len(each_query_result_list)):
        file_index = str(each_query_result_list[j])
        # print('who will cite: ', file_index)
        docID_of_citation_list = paragraph_citation.getCitationList(file_index, citation_graph, docID2citeID, citeID2docID)
        print('docID_of_citation_list: ', docID_of_citation_list)
        print(str(queries[i]))

        # Consider the entirety of queries[i] as paragraph citation key_query
        # key_query_str = ''
        # for sub_query in queries[i]:
        #     key_query_str += sub_query
        #     key_query_str += ' '
        # print('key_query_str: ', key_query_str)
        # paragraph_citation.iterateCitation(specific_citation_dir, text_dir, file_index, docID_of_citation_list, key_query=key_query_str)

        # Consider sub query as paragraph citation key_query
        for sub_query in queries[i]:
            print('sub_query: ', sub_query)
            in_degree_citation_weight_dict_paragraph, out_degree_citation_weight_dict_paragraph = paragraph_citation.iterateCitation(specific_citation_dir, text_dir, file_index, each_query_result_list,
                                                                       docID_of_citation_list, sub_query,
                                               in_degree_citation_weight_dict_paragraph, out_degree_citation_weight_dict_paragraph,
                                               simple_final_score_dict)

    print('in_degree: ', in_degree_citation_weight_dict_paragraph)
    print('out_degree: ', out_degree_citation_weight_dict_paragraph)

    out_degree_citation_weight_dict2list_paragraph = []
    in_degree_citation_weight_dict2list_paragraph = []
    for (k, v) in out_degree_citation_weight_dict_paragraph.items():
        out_degree_citation_weight_dict2list_paragraph.append([int(k), v])
    for (k, v) in in_degree_citation_weight_dict_paragraph.items():
        in_degree_citation_weight_dict2list_paragraph.append([int(k), v])
    # out_degree_citation_weight_dict2list = list(out_degree_citation_weight_dict)
    # print(out_degree_citation_weight_dict2list)
    normalized_out_degree_citation_weight_dict_paragraph = dict(normalization.normalize_list(out_degree_citation_weight_dict2list_paragraph))
    normalized_in_degree_citation_weight_dict_paragraph = dict(normalization.normalize_list(in_degree_citation_weight_dict2list_paragraph))

    print('normalized_out_degree_citation_weight_dict_paragraph: ', normalized_out_degree_citation_weight_dict_paragraph)
    print('normalized_in_degree_citation_weight_dict_paragraph: ', normalized_in_degree_citation_weight_dict_paragraph)

    print()
        # break
    # break






# ------------------------------------------------------------------------------------



# file_index = str(108173)
# # file_index = str(110585)
#
# docID_of_citation_list = paragraph_citation.getCitationList(file_index, citation_graph, docID2citeID, citeID2docID)
# print('docID_of_citation_list: ', docID_of_citation_list)
#
# # cited_file_name = text_dir + file_index + '.txt'
# keyQuery = "United"
# paragraph_citation.iterateCitation(specific_citation_dir, text_dir, file_index, docID_of_citation_list, keyQuery)

# cited_file_index = str(103846)
# paragraph_citation.getChar(specific_citation_dir, text_dir, file_index, docID_of_citation_list)




# print(citation_graph[file_index])


# print(len(citeID2docID))
# print(len(docID2citeID))
# print(type(citation_graph))