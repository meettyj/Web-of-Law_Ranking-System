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

citation_dir = './data/citation/'
citation_graph = citation.get_citation_graph(citation_dir)
docID2citeID, citeID2docID = citation.get_docID2citeID_and_citeID2docID(citation_dir)

specific_citation_dir = './data/all_scotus_NYU_IE1/'
text_dir = './data/all_scotus_text/'
file_index = str(108173)
# file_index = str(110585)

docID_of_citation_list = paragraph_citation.getCitationList(file_index, citation_graph, docID2citeID, citeID2docID)
print('docID_of_citation_list: ', docID_of_citation_list)

cited_file_name = text_dir + file_index + '.txt'
with open(cited_file_name, 'r') as f:
    # text = f.read()
    # print(text[3903:3928])
    charCounter = 0
    for line in f.readlines():
        if charCounter + len(line) >= 3928:
            # find key query in this line
            if "Amendment" in line:
                print('The key query is in the cited paragraph')
            else:
                print('Cannot find key query in the cited paragraph')
            break
        else:
            charCounter += len(line)

# cited_file_index = str(103846)
# paragraph_citation.getChar(specific_citation_dir, text_dir, file_index, docID_of_citation_list)




# print(citation_graph[file_index])


# print(len(citeID2docID))
# print(len(docID2citeID))
# print(type(citation_graph))