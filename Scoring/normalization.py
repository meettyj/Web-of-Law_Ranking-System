# Input list: [file_index, data_to_be_normalized]
# Output: [file_index, data_after_normalized]
import numpy as np
def normalize_list (list):
    # print(list)
    s = np.sum(list,axis = 0)[1]
    # print(s)
    normalized_list = [[file_index, score/s] for (file_index, score) in list]
    return normalized_list