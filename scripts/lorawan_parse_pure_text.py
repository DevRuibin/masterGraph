"""
Parse the pure text file to json format: each line is a json object
"""

import json
import os

file_path = "../data/lorawanPureText/OutSideEPL"
baseName = os.path.basename(file_path)

with open(file_path, "r") as fp:
    data = fp.readlines()
    for i in range(len(data)):
        data[i] = data[i].replace("\n", "")
        json_object = json.loads(data[i])
        new_json_file = f"../data/lorawan/{baseName}_{i}.json"
        with open(new_json_file, "w") as f:
            json.dump(json_object, f, indent=4)
            print(f"File {new_json_file} created")

