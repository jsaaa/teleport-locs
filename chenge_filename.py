import json

for i in range(14):

    json_open = open(str(i + 47) + ".json", 'r')
    json_load = json.load(json_open)

    json_load['name'] = i + 51

    with open("new\\" + str(i + 51) + ".json", mode='wt', encoding='utf-8') as file:
        json.dump(json_load, file, ensure_ascii=False)
                


#print(json_load['labels']['16']['name'])