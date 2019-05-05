import os
import json

quries = os.listdir("annotation_503")
# quries.remove(".DS_Store")

with open("data.input.503", "w") as ipf:
    for query in quries:
        # print(query)
        file_path_surffix = "annotation_503/{}/".format(query)
        root, dirs, files = list(os.walk(file_path_surffix))[0]
        for docid_txt in files:
            docid = docid_txt.replace(".txt", "")
            with open(file_path_surffix+docid_txt) as f:
                file_content = "docid: {}.txt\n".format(docid)
                file_content += "Query: {}".format(query)
                file_content += "\n---------------------- artical ----------------------\n\n"
                file_content += f.read()
                a = json.dumps({"text": file_content, "docid": docid, "query":query})
                ipf.write(a+"\n")
