import json
json_open = open('map_teyvat.json', 'r')
json_load = json.load(json_open)

farm = ["CrystalChunk"]
data = dict()

for farm_neme in farm:

    for labels in json_load['labels'].values():

        if labels['clear_name'] == farm_neme:

            for point in labels['points']:
                
                file_name = farm_neme + "_" + str(point['id'])

                data['description'] = ""
                data['name'] = file_name
                data['position'] = [point['y_pos'], 500, -point['x_pos']]

                with open(file_name + '.json', mode='wt', encoding='utf-8') as file:
                    json.dump(data, file, ensure_ascii=False)


#print(json_load['labels']['16']['name'])