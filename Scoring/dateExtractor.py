

def date_extract_from_single_file(date_dir, file_index):
    # docs_date_list = []
    file_name = date_dir + file_index + '.NYU_IE1'
    with open(file_name, 'r') as f:
        for line in f.readlines():
            if line[1:5] == "DATE":
                date_of_each_file = line.split('>')[1].split('<')[0]
                return date_of_each_file
                # docs_date_list.append(date_of_each_file)
                # print(date_each_file)
                # break
    return -1 # indicates we cannot find a date in this file




