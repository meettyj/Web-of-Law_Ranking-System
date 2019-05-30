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
# from Scoring import paragraph_citation

citation_dir = './data/citation/'
citation_graph = citation.get_citation_graph(citation_dir)
docID2citeID, citeID2docID = citation.get_docID2citeID_and_citeID2docID(citation_dir)

specific_citation_dir = './data/all_scotus_NYU_IE1/'
file_index = str(108173)

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
        print('docID_of_citation_list: ', docID_of_citation_list)

# print(citation_graph[file_index])


# print(len(citeID2docID))
# print(len(docID2citeID))
# print(type(citation_graph))