import json
import csv

with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["docid","annotation","user"])
    
    with open("ede.json") as f:
        for json_object in f:
            d=json.loads(json_object)
            d.pop("text")
            # print(d)
            if len(d['labels'])==1:
                writer.writerow([d['metadata']["docid"], d['labels'][0], d["username"]])
