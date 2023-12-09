import json
import glob
import os

file_names = glob.glob("Farming - Bird Egg/*.txt")
item_name = "BirdEgg"

if not os.path.exists(item_name + "/"):
    os.mkdir(item_name + "/")

cnt = 0
for file_name in file_names:

    data = dict()
    points=[0,0,0]
    
    with open(file_name, mode='r') as f:
        lines = f.readlines()

        for i in range(3):
            spl = lines[i+1].split('=')
            points[i] = float(spl[1])

    data['description'] = ""
    data['name'] = str(cnt)
    data['position'] = points[0], points[2], points[1]
    
    with open(item_name + "/" + str(cnt) + '.json', mode='wt', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    cnt = cnt + 1