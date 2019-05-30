
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

# we find to find specific paragraph
def getChar(specific_citation_dir, text_dir, file_index, docID_of_citation_list):
    # check if this file cite other files or not
    if len(docID_of_citation_list) == 0:
        print('this file doesn\'t cites any other file')
        return
    # go through NYU_IE1 file to find specific citation information
    file_name = specific_citation_dir + file_index + '.NYU_IE1'
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line[1:9] == "CITATION":
                # extract cited file id first
                cited_file_index = line.split('id1="')[1].split('"')[0]
                # check cited_file_index in citation list
                if cited_file_index in docID_of_citation_list:
                    cited_file_name = text_dir + file_index + '.txt'



                    print(cited_file_index)



                # go to the cited_file related paragraph to find key query.

    return


    # given file_index, find related NYUIE1 file





# def getChar(NYUIE1):