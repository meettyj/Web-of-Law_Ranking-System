
def getCitationList(file_index, citation_graph, docID2citeID, citeID2docID):
    if file_index not in docID2citeID:
        print('we cannot find %d.txt in citation graph' % (file_index))
        # then we set it's citation weight as 0
        return []
    else:
        who_will_cite = str(docID2citeID[file_index])
        print('which_doc_will_cite: ', file_index)
        # for who_will_cite in citeIDlist:
        if who_will_cite not in citation_graph:
            print('2. we cannot find %d.txt in citation graph' % (file_index))
            return []
            # # who_will_cite = float(str(who_will_cite) + '.001')
            # who_will_cite = str(who_will_cite).split('.')[0]
            # print(who_will_cite)
            # print('remove .001: ', citation_graph[who_will_cite])
        else:
            # print('citeID: ', who_will_cite)
            citation_list = citation_graph[who_will_cite]
            # print('citation_list: ', citation_list)
            docID_of_citation_list = [citeID2docID[citeID] for citeID in citation_list if citeID in citeID2docID]
            return docID_of_citation_list

# we need to find specific paragraph
def iterateCitation(specific_citation_dir, text_dir, file_index, each_query_result_list, docID_of_citation_list, key_query, in_degree_citation_weight_dict_paragraph,
                                              out_degree_citation_weight_dict_paragraph, simple_final_score_dict):
    in_degree_update = in_degree_citation_weight_dict_paragraph
    out_degree_update = out_degree_citation_weight_dict_paragraph
    cited_file_dictionary = set()
    # check if this file cite other files or not
    if len(docID_of_citation_list) == 0:
        print('1. this file doesn\'t cites any other file')
        return in_degree_update, out_degree_update
    # check if this file cite any file that in the result of BM25
    # print()
    # print('each_query_result_list: ', each_query_result_list)
    # print('docID_of_citation_list: ', docID_of_citation_list)
    docID_of_citation_list_intersection = getIntersectionList(each_query_result_list, docID_of_citation_list)
    print('Intersection: ', docID_of_citation_list_intersection)
    if len(docID_of_citation_list_intersection) == 0:
        print('2. this file doesn\'t cites any other file')
        return in_degree_update, out_degree_update

    # go through NYU_IE1 file to find specific citation information
    file_name = specific_citation_dir + file_index + '.NYU_IE1'
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line[1:9] == "CITATION":
                # extract cited file id first
                cited_file_index = line.split('id1="')[1].split('"')[0]
                # print('cited_file_index_tmp: ', cited_file_index)

                # check cited_file_index in citation list
                if cited_file_index not in cited_file_dictionary and cited_file_index in docID_of_citation_list_intersection:
                    # get end index of specific citation
                    endIndex = getEndIndex(line)


                    cited_file_name = text_dir + cited_file_index + '.txt'
                    # go to the cited_file related paragraph to find key query.
                    findOrNot = iterateParagraph(cited_file_name, key_query, endIndex)
                    # print(findOrNot)
                    if findOrNot:
                        in_degree_update,out_degree_update = \
                            countCitationWeight(file_index, cited_file_index, in_degree_update,
                                                  out_degree_update, simple_final_score_dict)




                    # print('cited_file_index: ', cited_file_index)
                cited_file_dictionary.add(cited_file_index)
    return in_degree_update, out_degree_update

# find end index in citation line of file NYU_IE1
def getEndIndex(citationLine):
    # print(citationLine)
    endIndex = citationLine.split('end="')[1].split('"')[0]
    # print('endIndex: ', endIndex)
    return endIndex

# Iterate paragraph of cited file to find key query. Return boolean.
def iterateParagraph(cited_file_name, key_query, endIndex):
    with open(cited_file_name, 'r') as f:
        # text = f.read()
        # print(text[3903:3928])
        charCounter = 0
        for line in f.readlines():
            if charCounter + len(line) >= int(endIndex):
                # find key query in this line
                if key_query in line:
                    print('!!!! Find !!!! The key query "%s" is in the cited paragraph of cited document "%s"' %(key_query, cited_file_name))
                    return True
                else:
                    print('--- Cannot find --- key query: "%s", cited document: "%s"' %(key_query, cited_file_name))
                    return False
            else:
                charCounter += len(line)
        # Actually we should not arrive here. If we are here, then there are some fault in SCOTUS text file occurs.
        # Thus, we will return False, indicating we cannot find key query in cited document.
        # print('charCounter: ', charCounter)
        print('--- Wrong --- The citation endIndex exceed file "%s" length.' %(cited_file_name))
        return False

    # given file_index, find related NYUIE1 file

def countCitationWeight(file_index, query_result, in_degree_citation_weight_dict_paragraph, out_degree_citation_weight_dict_paragraph, simple_final_score_dict):
    cite_index_weight = 1
    # out_degree_citation_weight_dict_paragraph[query_result] += cite_index_weight * simple_final_score_dict[
    #     int(file_index)]  # you will add my importance
    # in_degree_citation_weight_dict_paragraph[file_index] += cite_index_weight * simple_final_score_dict[
    #     int(query_result)]  # I will add your importance
    out_degree_citation_weight_dict_paragraph[query_result] += cite_index_weight # you will add my importance
    in_degree_citation_weight_dict_paragraph[file_index] += cite_index_weight # I will add your importance

    return in_degree_citation_weight_dict_paragraph, out_degree_citation_weight_dict_paragraph

def getIntersectionList(list_A, list_B):
    intersectionList = [i for i in list_A if i in list_B]
    return intersectionList


    # def getChar(NYUIE1):