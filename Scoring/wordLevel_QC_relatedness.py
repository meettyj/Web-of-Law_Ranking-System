import os
import sys
import time
import numpy as np
import pickle
import gensim


def calc_wordLevel_QC_relatedness_score(query_embedding, doc_embedding):
    # pretrained_embedding_path = "../word2vec/GoogleNews-vectors-negative300.bin"
    query_array = np.array(query_embedding) # length of query * 300
    doc_array = np.array(doc_embedding) # length of doc * 300
    # print('shape of query array: ', query_array.shape)
    # print('shape of doc array: ', doc_array.shape)

    # The relation score between each word in doc and each word in query.
    score_array = np.dot(doc_array, query_array.transpose()) # length of doc * length of query.
    # print('shape of score array: ', score_array.shape)
    score_before_normalization = score_array.sum()
    # print('score before normalization: ', score_before_normalization)
    score = score_before_normalization/len(score_array)
    return score


# def get_query_embedding(queries, pretrained_embedding_fpath):
#     for i in range(len(queries)):
#         for j in range(len(queries[i])):
#             print(queries[i][j])
            # get_embeddings_from_pretrained_googlenews_w2v(queries[i][j])

# def get_corpus_embedding(each_corpus_text_list, pretrained_embedding_fpath):

def get_embeddings_from_pretrained_googlenews_w2v(text_list, model):
    doc_embedding = []

    found_cnt = 0
    not_found_cnt = 0
    # words = []
    for word in text_list:
        # words.append(word)
        if word in model.vocab:
            doc_embedding.append(model.word_vec(word))
            found_cnt += 1
        else:
            # to include word_in_vocab or not
            not_in_vocab_random_vector = np.random.uniform(-0.25, 0.25, 300)
            doc_embedding.append(not_in_vocab_random_vector)
            not_found_cnt += 1

    # print('length of text_list: ', len(text_list))
    # print('how many has been found: ', found_cnt)
    # print('not found: ', not_found_cnt)

    return doc_embedding

    # with open(fpath_pretrained_extracted, 'wb') as f:
    #     pickle.dump(embedding_weights, f)
    # with open(fpath_word_list, 'w') as f:
    #     f.write("\n".join(words))








