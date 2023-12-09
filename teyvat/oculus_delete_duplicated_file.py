import json
import glob
import numpy
import csv
import shutil
import datetime
import os

items = ["Anemoculus","CrimsonAgate","Geoculus","Electroculus","Dendroculus"]

dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

with open('アイテム名.csv') as f:
    reader = csv.DictReader(f)
    item_list_tmp = [row for row in reader]

print("Backup...")
for item_name in items:
    shutil.copytree(item_name, "backup_" + dt_now + "/" + item_name)
print("Done")

json_list = []
    
for item_name in items:

    file_names_tmp = glob.glob(item_name + "/*.json")

    for file_name in file_names_tmp:
        json_open = open(file_name, 'r')
        json_load = json.load(json_open)
        json_list.append(json_load)
        json_list[-1]["filename"] = file_name

dupeindex = []
for index_curpos, json_file_curpos in enumerate(json_list):
    
    if not index_curpos in dupeindex:

        for index, json_file in enumerate(json_list):
            if (not index_curpos == index and
                not index in dupeindex and
                numpy.sqrt(pow(json_file['position'][0] - json_file_curpos['position'][0],2) + pow(json_file['position'][2] - json_file_curpos['position'][2],2)) < 0.2 and
                abs(json_file['position'][1] - json_file_curpos['position'][1]) < 0.2):
                print(json_file_curpos['filename'] + " ============ " + json_file['filename'])
                dupeindex.append(index)

for i in dupeindex:
    if os.path.exists(json_list[i]['filename']):
        os.remove(json_list[i]['filename'])