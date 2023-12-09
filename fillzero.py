import json
import glob

path = "teleports/全て/"
init_num = 0

file_names = glob.glob(path + "*.json")

for file_name in file_names:
    
    splited = file_name.split('/')[-1].split('\\')[1]
    num = splited.split('_')[0]

    json_open = open(file_name, 'r')
    json_load = json.load(json_open)

    filledzero = num.zfill(4)
    json_load['name'] = filledzero

    with open(path + splited.replace(str(num) + "_", filledzero + "_"), mode='wt', encoding='utf-8') as file:
        json.dump(json_load, file, ensure_ascii=False)
            