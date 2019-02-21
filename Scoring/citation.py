import pandas as pd

# import numpy as np
# def normalize_list (list):
#     # print(list)
#     s = np.sum(list,axis = 0)[1]
#     # print(s)
#     normalized_list = [[file_index, score/s] for (file_index, score) in list]
#     return normalized_list

# still keep the ranking order
def remove_duplicate_and_self(self_value, input_list):
    temp_list=[]
    for one in input_list:
        if one not in temp_list:
            if one != self_value:
                temp_list.append(one)
    return temp_list

# return: dict
def get_citation_graph(citation_file_address):
    citation_dir = citation_file_address
    citation_graph_file_name = citation_dir + 'scotus.citation_graph'
    citation_graph = {}
    with open(citation_graph_file_name, 'r') as f:
        for line in f.readlines():
            # id = line.split(':')[0].split('.')[0]
            id = line.split(':')[0].split('.')[0]
            content = line.split(':')[1].split(' ')[1:-1]
            content = [item.split('.')[0] for item in content]
            content = remove_duplicate_and_self(id, content)
            # if len(id.split('.')) == 1:
            #     id = id + '.001'
            citation_graph[id] = content
    # for i in range(10):
    #     print('citation_graph: ', citation_graph.popitem())
    return citation_graph

def get_docID2citeID_and_citeID2docID(citation_file_address):
    citation_dir = citation_file_address
    table_citation_file_name = citation_dir + 'scotus_global_table_file.tsv'
    # rows_useful = [i for i in range(176462)]
    # we only need the first two column of the tsv table. After 176461 rows, it's all Dummy_file.
    table_citation = pd.read_csv(table_citation_file_name, sep='\t', nrows=176461, usecols=[1])
    # table_citation = pd.read_csv(table_citation_file_name, sep='\t', nrows=10, usecols=[1])
    citeID2docID = table_citation.to_dict()['id1']
    # transpose
    docID2citeID = dict((str(v), str(k).split('.')[0]) for k, v in citeID2docID.items())
    citeID2docID = dict((v, k) for k, v in docID2citeID.items())
    # for i in range(10):
    #     print('docID2citeID: ', docID2citeID.popitem())
    #     print('citeID2docID: ', citeID2docID.popitem())
    return docID2citeID, citeID2docID

def count_citation_weight(file_index, in_degree_citation_weight_dict, out_degree_citation_weight_dict, each_query_result_list, simple_final_score_dict, citation_graph, docID2citeID, citeID2docID, ever_met_file_list, cite_index):
    # cite_index_weight = None
    if cite_index == 1:
        cite_index_weight = 1
    elif cite_index == 2:
        cite_index_weight = 0.65
    elif cite_index == 3:
        cite_index_weight = 0.3
    else:
        print('We only consider cite index within 1, 2, 3')
        return -1
    in_degree_citation_weight_dict_update = in_degree_citation_weight_dict
    out_degree_citation_weight_dict_update = out_degree_citation_weight_dict
    next_cite_list = []
    ever_met_file_list_update = ever_met_file_list
    ever_met_file_list_update.append(file_index)

    if file_index not in docID2citeID:
        print('we cannot find %d.txt in citation graph' % (file_index))
        # then we set it's citation weight as 0
    else:
        who_will_cite = str(docID2citeID[file_index])
        print('which_doc_will_cite: ', file_index)
        # for who_will_cite in citeIDlist:
        if who_will_cite not in citation_graph:
            print('2. we cannot find %d.txt in citation graph' % (file_index))
            # # who_will_cite = float(str(who_will_cite) + '.001')
            # who_will_cite = str(who_will_cite).split('.')[0]
            # print(who_will_cite)
            # print('remove .001: ', citation_graph[who_will_cite])
        else:
            # print('citeID: ', who_will_cite)
            citation_list = citation_graph[who_will_cite]
            # print('citation_list: ', citation_list)
            docID_of_citation_list = [citeID2docID[citeID] for citeID in citation_list if citeID in citeID2docID]
            # print('docID_of_citation_list: ', docID_of_citation_list)
            # initialize the citation count
            # citation_count = [(item, 0.2) for item in each_query_result_list]
            for query_result in each_query_result_list:
                # given A. A cites B(in extracted files). out_degree: B increase importance
                if query_result in docID_of_citation_list:
                    # print(out_degree_citation_weight[query_result])
                    # print(simple_final_score_dict[query_result])
                    if query_result in ever_met_file_list_update:
                        break
                    else:
                        print('this doc has cite: ', query_result)
                        out_degree_citation_weight_dict_update[query_result] += cite_index_weight * simple_final_score_dict[int(file_index)] # you will add my importance
                        in_degree_citation_weight_dict_update[file_index] += cite_index_weight * simple_final_score_dict[int(query_result)] # I will add your importance
                        next_cite_list.append(query_result)
                        ever_met_file_list_update.append(query_result)
    return in_degree_citation_weight_dict_update, out_degree_citation_weight_dict_update, next_cite_list, ever_met_file_list_update

# normalized_out_degree_citation_weight_dict = {110585: 0.05705400687201952, 110117: 0.05705400687201952, 109093: 0.27178397251192177, 111977: 0.05705400687201952, 108785: 0.05705400687201952, 109775: 0.27178397251192177, 109258: 0.05705400687201952, 107693: 0.05705400687201952, 101183: 0.05705400687201952, 110896: 0.05705400687201952}
# normalized_in_degree_citation_weight_dict = {110585: 0.45912146861115627, 110117: 0.06009761459876039, 109093: 0.06009761459876039, 111977: 0.06009761459876039, 108785: 0.06009761459876039, 109775: 0.06009761459876039, 109258: 0.06009761459876039, 107693: 0.06009761459876039, 101183: 0.06009761459876039, 110896: 0.06009761459876039}
#
# simple_final_score_dict = dict([[110117, 0.6476683107747294], [107693, 0.4694015393566387], [108785, 0.46012723083510687], [110585, 0.37636263851121443], [101183, 0.3743445229007746], [110896, 0.3630108018095742], [109775, 0.34075692055145335], [111977, 0.33679462110294256], [109093, 0.3232026337111653], [109258, 0.3083307804464006]])
# print(simple_final_score_dict)
# # for
#
# six_feature_final_score = {}
# for id, score in simple_final_score_dict.items():
#     # print(id)
#     six_feature_final_score[id] = simple_final_score_dict[id] + normalized_out_degree_citation_weight_dict[int(id)] + \
#                                   normalized_in_degree_citation_weight_dict[int(id)]
# # print(six_feature_final_score)
# # transform dict to list, in order to sort
# six_feature_final_score = [[k, v] for (k, v) in six_feature_final_score.items()]
# print(six_feature_final_score)
# print(sorted(six_feature_final_score,reverse=True,key=lambda item: item[1]))

# out_degree_citation_weight_dict = {'110585': 0.1, '110117': 0.1, '109093': 0.47567663135271865, '111977': 0.1, '108785': 0.1, '109775': 0.47567663135271865, '109258': 0.1, '107693': 0.1, '101183': 0.1, '110896': 0.1}
# in_degree_citation_weight_dict = {'110585': 0.7627408494309137, '110117': 0.1, '109093': 0.1, '111977': 0.1, '108785': 0.1, '109775': 0.1, '109258': 0.1, '107693': 0.1, '101183': 0.1, '110896': 0.1}
# out_degree_citation_weight_dict2list = []
# for (k, v) in out_degree_citation_weight_dict.items():
#     out_degree_citation_weight_dict2list.append([int(k), v])
# # out_degree_citation_weight_dict2list = list(out_degree_citation_weight_dict)
# print(out_degree_citation_weight_dict2list)
# normalized_out_degree_citation_weight_dict = dict(normalize_list(out_degree_citation_weight_dict2list))
# print()
# print('normalized_out_degree_citation_weight_dict: ', normalized_out_degree_citation_weight_dict)
# print(len(normalized_out_degree_citation_weight_dict))

# each_query_result_list = ['110585', '110117', '109093', '111977', '108785', '109775', '109258', '107693', '101183', '110896']
# citation_dir = '../data/citation/'
# citation_graph = get_citation_graph(citation_dir)
#
# docID2citeID, citeID2docID = get_docID2citeID_and_citeID2docID(citation_dir)
#
#
# # for A -> B. in_degree means B. out_degree means A.
# # Initialization
# in_degree_citation_weight = [(str(item), 0.1) for item in each_query_result_list]
# out_degree_citation_weight = [(str(item), 0.1) for item in each_query_result_list]
# in_degree_citation_weight_dict = dict(in_degree_citation_weight)
# out_degree_citation_weight_dict = dict(out_degree_citation_weight)
#
# # comment
# sort_simple_final_score = [[110117, 0.6475784641789251], [107693, 0.47232458997219284], [108785, 0.45918693063272964], [110585, 0.37645615165690977], [101183, 0.3743726575626864], [110896, 0.3628536181516715], [109775, 0.3414006162224349], [111977, 0.3357395586387545], [109093, 0.32226445764667744], [109258, 0.30782295533701803]]
# sort_simple_final_score_dict = dict(sort_simple_final_score)
# print('sort_simple_final_score_dict: ', sort_simple_final_score_dict)
#
# # comment
# file_index = str(110585) # test
#
# # First cite chain
# in_degree_citation_weight_dict, out_degree_citation_weight_dict, next_cite_list, ever_met_file_list = count_citation_weight(file_index, in_degree_citation_weight_dict,
#                                                                                         out_degree_citation_weight_dict, docID2citeID, citeID2docID,[], 1)
# # Second cite chain
# for next_consider_query in next_cite_list:
#     in_degree_citation_weight_dict, out_degree_citation_weight_dict,next_cite_list,ever_met_file_list = count_citation_weight(next_consider_query, in_degree_citation_weight_dict,
#                                                                                             out_degree_citation_weight_dict, docID2citeID, citeID2docID,ever_met_file_list, 2)
# # Third cite chain
# for next_consider_query in next_cite_list:
#     in_degree_citation_weight_dict, out_degree_citation_weight_dict,_,_ = count_citation_weight(next_consider_query, in_degree_citation_weight_dict,
#                                                                                             out_degree_citation_weight_dict, docID2citeID, citeID2docID,ever_met_file_list, 3)
#
#
#
# print('out_degree_citation_weight: ', out_degree_citation_weight_dict)
# print('in_degree_citation_weight: ', in_degree_citation_weight_dict)













