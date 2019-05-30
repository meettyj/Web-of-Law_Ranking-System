
# we find to find specific paragraph
def getChar(specific_citation_dir, file_index):
    file_name = specific_citation_dir + file_index + '.NYU_IE1'
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line[1:9] == "CITATION":


    # given file_index, find related NYUIE1 file




# def getChar(NYUIE1):