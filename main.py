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

if __name__ == '__main__':
    length_BM25 = 20
    path_Query = './data/10_query_list.txt'
    # path_Corpus = './data/1K_scotus_corpus.txt'
    path_Corpus = './data/all_scotus_corpus.txt'
    # path_Corpus = './data/test_scotus_corpus.txt'

    queries, dict_BM25, dict_BM25_with_score = entry.main_BM25(path_Query, path_Corpus, length_BM25)
    print('queries: ', queries)
    print()
    print('dictionary for result after BM25: ', dict_BM25)
    print()

    # here we load word2vec model to save loading time. Will be change in the future.
    pretrained_embedding_path = "../word2vec/GoogleNews-vectors-negative300.bin"
    tic = time.time()
    print('Please wait ... (it could take a while to load the file : {})'.format(pretrained_embedding_path))
    model = gensim.models.KeyedVectors.load_word2vec_format(pretrained_embedding_path, binary=True)
    print('Done.  (time used: {:.1f}s)\n'.format(time.time()-tic))
    # embedding_dim = 300

    # initialize for Key Phrases Overlap (second part of Scoring)
    rake_object = Rake()

    corpus_dir = './data/all_scotus_text/'
    date_dir = './data/all_scotus_NYU_IE1/'
    for i in range(len(queries)):
    # for i in range(1): # for development setting
        print('============================== Query{}: {} =================================='.format(i+1, queries[i]))
        # BM25 score weight list
        # print('dict_BM25_with_score: ', dict_BM25_with_score)
        # print(dict_BM25_with_score[i])
        normalized_BM25_weight_list = normalization.normalize_list(dict_BM25_with_score[i])
        print('BM25 weight list: ',normalized_BM25_weight_list)
        # print()

        each_query_result_list = dict_BM25.get(i, 0)
        # print(each_query_result_list) # docs ID
        embedding_each_query = wordLevel_QC_relatedness.get_embeddings_from_pretrained_googlenews_w2v(queries[i], model)
        # print('length of query embedding: ', len(embedding_each_query))

        # test = [[1,0.7],[2,1.4],[3,0.7]]
        # print(normalization.normalize_list(test))

        # word level QC relatedness part & Key Phrases overlap part.
        # Output word_level_QC_relatedness_weight[file_index, score_word_level_QC]
        # Output
        word_level_QC_relatedness_weight = []
        key_phrases_overlap_weight = []
        for j in range(len(each_query_result_list)):
            file_index = str(each_query_result_list[j])
            file_name = corpus_dir + file_index + '.txt'

            # print(str(each_query_result_list[j]))

            # print('The score for {} in Scotus'.format(file_name.split('/')[3]))
            with open(file_name, 'r') as f:
                doc_text = f.read().lower()
                each_doc_text = doc_text.split()

                # word level QC relatedness score
                embedding_each_doc = wordLevel_QC_relatedness.get_embeddings_from_pretrained_googlenews_w2v(each_doc_text, model)
                # print('length of doc embedding: ', len(embedding_each_doc))
                score_word_level_QC = wordLevel_QC_relatedness.calc_wordLevel_QC_relatedness_score(embedding_each_query, embedding_each_doc)
                word_level_QC_relatedness_weight.append([int(file_index), score_word_level_QC])
                # print('each doc word level QC relatedness score: ', score_word_level_QC)

                # Key Phrases overlap between query and docs
                score_KP = 0
                rake_object.extract_keywords_from_text(doc_text)
                # Here we consider only top 20 results. and using the score generated by RAKE algorithm. decayed on each position with ratio 0.95.
                top_n_result_RAKE = 20
                result_list_RAKE = rake_object.get_ranked_phrases_with_scores()[:top_n_result_RAKE] # get_ranked_phrases() to ignore score.
                # print('Key Phrases extracted with Rake algorithm: ', result_list_RAKE)
                decay_factor = 1
                ratio_to_decay = 0.95
                combined_item_in_query = ''.join(queries[i])
                total_match_factor = 1.5
                for score_RAKE, KP_RAKE in result_list_RAKE:
                    if combined_item_in_query in KP_RAKE:
                        score_KP += total_match_factor * score_RAKE * decay_factor
                    else:
                        for item in queries[i]:
                            if item in KP_RAKE:
                                score_KP += score_RAKE * decay_factor
                                break # we only consider one match in query at most for now.
                    decay_factor *= ratio_to_decay
                key_phrases_overlap_weight.append([int(file_index), score_KP+5.0])
                # print('each doc Key Phrases overlap score: ', score_KP)
                # print()

        normalized_word_level_relatedness_weight_list = normalization.normalize_list(word_level_QC_relatedness_weight)
        normalized_KP_overlap_weight_list = normalization.normalize_list(key_phrases_overlap_weight)
        print('word level QC relatedness weight score: ', normalized_word_level_relatedness_weight_list)
        # print()
        print('Key Phrases overlap weight score: ', normalized_KP_overlap_weight_list)
        # print()

        # Date part. Output list[date, file_index, weight]
        docs_date_list = []
        for m in range(len(each_query_result_list)):
            file_index = str(each_query_result_list[m])
            # file_name = corpus_dir + file_index + '.txt'
            # file_name = corpus_dir + str(each_query_result_list[j]) + '.txt'

            # Date Part
            # date_file_name = date_dir + str(each_query_result_list[j]) + '.NYU_IE1'

            date_of_each_file = dateExtractor.date_extract_from_single_file(date_dir, file_index)
            # if date_of_each_file != -1:
            if type(date_of_each_file) != int and len(date_of_each_file.split(', ')) != 1:
                docs_date_list.append([date_of_each_file.split(',')[1],file_index])
            else:
                docs_date_list.append([str(date_of_each_file),file_index])
        # print('docs_date_list: ', docs_date_list)
        sort_docs_date_list = sorted(docs_date_list, reverse=True)
        date_weight = 1
        date_decay_factor = 0.05
        for k in range(len(sort_docs_date_list)):
            date = sort_docs_date_list[k][0]
            if date != -1:
                sort_docs_date_list[k].append(date_weight) # include human given weight
                date_weight -= date_decay_factor
            else:
                sort_docs_date_list[k].append(0.75) # To deal with those file without date, we give an average score. Based on 10 extracted files, we give 0.75.
        # print('date_fileIndex_weight list: ', sort_docs_date_list)
        prepared_for_normalized_date_list = [[int(x[1]), x[2]] for x in sort_docs_date_list] # to remove the date from list
        # print(prepared_for_normalized_date_list)
        normalized_date_weight_list = normalization.normalize_list(prepared_for_normalized_date_list)
        print('Date weight list: ', normalized_date_weight_list)
        print()

        # Total score
        final_score = {}

        # So for now. We have 4 weight list.
        # normalized_BM25_weight_list, normalized_word_level_relatedness_weight_list, normalized_KP_overlap_weight_list, normalized_date_weight_list

        for [id, weight_score] in normalized_BM25_weight_list:
            final_score[id] = [[weight_score],weight_score]
        for [id, weight_score] in normalized_word_level_relatedness_weight_list:
            final_score[id][0].append(weight_score)
            final_score[id][1] += weight_score
        for [id, weight_score] in normalized_KP_overlap_weight_list:
            final_score[id][0].append(weight_score)
            final_score[id][1] += weight_score
        for [id, weight_score] in normalized_date_weight_list:
            final_score[id][0].append(weight_score)
            final_score[id][1] += weight_score

        print('final_score: ', final_score)
        print()

        # simple format of final score only contains file id and weight score.
        simple_final_score = []
        for id in final_score:
            simple_final_score.append([id, final_score[id][1]])
        # print('simple_final_score: ', simple_final_score)
        # print()

        # to sort the final score.
        sort_simple_final_score = sorted(simple_final_score,reverse=True,key=lambda item: item[1])
        print('sorted final_score simple format: ', sort_simple_final_score)
        print()


        # Citation part
        citation_dir = './data/citation/'
        citation_graph = citation.get_citation_graph(citation_dir)
        docID2citeID, citeID2docID = citation.get_docID2citeID_and_citeID2docID(citation_dir)

        # for A -> B. in_degree means B. out_degree means A.
        # Initialization
        in_degree_citation_weight = [(str(item), 0.1) for item in each_query_result_list]
        out_degree_citation_weight = [(str(item), 0.1) for item in each_query_result_list]
        in_degree_citation_weight_dict = dict(in_degree_citation_weight)
        out_degree_citation_weight_dict = dict(out_degree_citation_weight)

        simple_final_score_dict = dict(sort_simple_final_score)
        # print('simple_final_score_dict: ', simple_final_score_dict)

        ever_met_file_list = []
        for j in range(len(each_query_result_list)):
            file_index = str(each_query_result_list[j])
            # First cite chain
            in_degree_citation_weight_dict, out_degree_citation_weight_dict, next_cite_list, ever_met_file_list = citation.count_citation_weight(file_index, in_degree_citation_weight_dict,
                                                                                                    out_degree_citation_weight_dict, each_query_result_list, simple_final_score_dict, citation_graph, docID2citeID, citeID2docID, ever_met_file_list, 1)
            # print('1. ever_met_file_list: ', ever_met_file_list)
            ever_met_file_list = list(set(ever_met_file_list))
            # Second cite chain
            for next_consider_query in next_cite_list:
                in_degree_citation_weight_dict, out_degree_citation_weight_dict,next_cite_list,ever_met_file_list_update = citation.count_citation_weight(next_consider_query, in_degree_citation_weight_dict,
                                                                                                        out_degree_citation_weight_dict, each_query_result_list, simple_final_score_dict, citation_graph, docID2citeID, citeID2docID, ever_met_file_list, 2)
                ever_met_file_list.extend(ever_met_file_list_update)
                ever_met_file_list = list(set(ever_met_file_list))
            # print('2. ever_met_file_list: ', ever_met_file_list)
            # Third cite chain
            for next_consider_query in next_cite_list:
                in_degree_citation_weight_dict, out_degree_citation_weight_dict,_,_ = citation.count_citation_weight(next_consider_query, in_degree_citation_weight_dict,
                                                                                                        out_degree_citation_weight_dict, each_query_result_list, simple_final_score_dict, citation_graph, docID2citeID, citeID2docID, ever_met_file_list, 3)
        # print('ever_met_file_list: ', ever_met_file_list)

        print('out_degree_citation_weight: ', out_degree_citation_weight_dict)
        print('in_degree_citation_weight: ', in_degree_citation_weight_dict)
        print()

        out_degree_citation_weight_dict2list = []
        in_degree_citation_weight_dict2list = []
        for (k, v) in out_degree_citation_weight_dict.items():
            out_degree_citation_weight_dict2list.append([int(k), v])
        for (k, v) in in_degree_citation_weight_dict.items():
            in_degree_citation_weight_dict2list.append([int(k), v])
        # out_degree_citation_weight_dict2list = list(out_degree_citation_weight_dict)
        # print(out_degree_citation_weight_dict2list)
        normalized_out_degree_citation_weight_dict = dict(normalization.normalize_list(out_degree_citation_weight_dict2list))
        normalized_in_degree_citation_weight_dict = dict(normalization.normalize_list(in_degree_citation_weight_dict2list))

        print('normalized_out_degree_citation_weight_dict: ', normalized_out_degree_citation_weight_dict)
        print('normalized_in_degree_citation_weight_dict: ', normalized_in_degree_citation_weight_dict)
        print()

        # normalized_out_degree_citation_weight_dict = dict(normalization.normalize_list(list(out_degree_citation_weight_dict)))
        # normalized_in_degree_citation_weight_dict = dict(normalization.normalize_list(list(in_degree_citation_weight_dict)))
        # print()
        # print('normalized_out_degree_citation_weight_dict: ', normalized_out_degree_citation_weight_dict)
        # print('normalized_in_degree_citation_weight_dict: ', normalized_in_degree_citation_weight_dict)


        # ---------------------------------------------------------------------------------------------------------------------------------------
        # Paragraph citation part
        # citation_dir = './data/citation/'
        # citation_graph = citation.get_citation_graph(citation_dir)

        # Paragraph citation part
        print('--------------------- Start of paragraph citation part ---------------------')
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







        # ---------------------------------------------------------------------------------------------------------------------------------------


        six_feature_final_score_dict = {}
        for id, score in simple_final_score_dict.items():
            # print(id)
            six_feature_final_score_dict[id] = simple_final_score_dict[id] + normalized_out_degree_citation_weight_dict[int(id)] + \
                                          normalized_in_degree_citation_weight_dict[int(id)]
        # print(six_feature_final_score)
        # transform dict to list, in order to sort
        six_feature_final_score = [[k, v] for (k, v) in six_feature_final_score_dict.items()]
        # print(six_feature_final_score)
        print('SIX FEATURE COMBINED FINAL SCORE: ', sorted(six_feature_final_score, reverse=True, key=lambda item: item[1]))
        print()

        # After incorporating the paragraph citaion
        seven_feature_final_score_dict = {}
        for id, score in six_feature_final_score_dict.items():
            # print(id)
            seven_feature_final_score_dict[id] = six_feature_final_score_dict[id] + normalized_out_degree_citation_weight_dict_paragraph[
                int(id)] + \
                                            normalized_in_degree_citation_weight_dict_paragraph[int(id)]
        # print(six_feature_final_score)
        # transform dict to list, in order to sort
        seven_feature_final_score = [[k, v] for (k, v) in seven_feature_final_score_dict.items()]
        # print(six_feature_final_score)
        print('SEVEN FEATURE COMBINED FINAL SCORE: ', sorted(seven_feature_final_score, reverse=True, key=lambda item: item[1]))
        print()
        # break






