import json
import glob
import numpy
import csv
import os

maps = ["teyvat"]  #回る順番

#items = ["CrystalChunk", "AmethystLump", "artifact", "elite600", "AbyssMage", "FatuiAgent", "FatuiCicinMage", "FatuiMirrorMaiden", "GeovishapHatchling", "Mitachurl", "RuinDrake", "RuinGuard", "RuinHunter", "RuinSentinel", "WolvesOfTheRiht", "Crab", "Berry", "Matsutake", "Mint", "Pine", "RawMeat", "SmallLampGrass", "SunsetFluit", "SweetFlower"]  #回収するもの　全て
#items = ["elite600", "AbyssMage", "FatuiAgent", "FatuiCicinMage", "FatuiMirrorMaiden", "GeovishapHatchling", "Mitachurl", "RuinDrake", "RuinGuard", "RuinHunter", "RuinSentinel", "WolvesOfTheRiht"]	#敵のみ
#items = ["CommonChest","ExquisiteChest","PreciousChest","LuxuriousChest","Seelie","TimeTrialChallenge", "CrimsonAgate"]  #宝箱、仙霊、時限挑戦
#items = ["elite600", "AbyssMage", "FatuiAgent", "FatuiCicinMage", "FatuiMirrorMaiden", "GeovishapHatchling", "Mitachurl", "RuinDrake", "RuinGuard", "RuinHunter", "RuinSentinel", "WolvesOfTheRiht", "Crab", "Berry", "Matsutake", "Mint", "Pine", "RawMeat", "SmallLampGrass", "SunsetFluit", "SweetFlower"]  #日課

#聖遺物 前　 1148
#聖遺物 後　 1277
#聖遺物 獲得 129

current_position = [3048, 300, 194]     #スタート位置
distance_max = 999999999999             #スタート位置を基準に半径がこの値の円の内側からアイテムを取得する 無効にする場合:inf

#current_position = {"x":1085, "y":"300", "z":-826}
#distance_max = numpy.sqrt(pow(999 - current_position["x"],2) + pow(-1484 - current_position["z"],2))

exclusion_distance = 1          #アイテム同士の距離がこの値以下なら除外 無効にする場合:-1
loading_distance = 100          #テレポート毎にロードをはさむための距離。この距離以上テレポートするとロードをはさむ 無効にする場合:-1

items = []
with open('teyvat/アイテム名.csv') as f:
    reader = csv.DictReader(f)
    item_list_tmp = [row for row in reader]

copy_dir_name = "teleports/"
item_names_JA = ""
print("items = ")
for ilt in item_list_tmp:
    if ilt["read"] == "TRUE":
        print("\t" + ilt["english"])
        items.append(ilt["english"])
        item_names_JA += ilt["japanese"] + "、"

item_names_JA = item_names_JA[:20]

if item_names_JA[-1] == "、":
    item_names_JA = item_names_JA[:-1]

item_names_JA += "/"
copy_dir_name += item_names_JA

if os.path.exists(copy_dir_name):
    file_list_in_copy_dir = glob.glob(copy_dir_name + "*.json")
    if file_list_in_copy_dir:
        print("Some .json file already exists at the copy folder.")
        exit()
else:
    os.mkdir(copy_dir_name)

file_names = []
json_list = []
for map_name in maps:
    
    for item_name in items:

        file_names_tmp = glob.glob(map_name + "/" + item_name + "/*.json")

        for file_name in file_names_tmp:
            json_open = open(file_name, 'r')
            json_load = json.load(json_open)
            if numpy.sqrt(pow(json_load['position'][0] - current_position[0],2) + pow(json_load['position'][2] - current_position[2],2)) < distance_max:
                json_list.append(json_load)
                json_list[-1]["english"] = item_name
                json_list[-1]["filename"] = file_name

json_list_copy = json_list
current_position_copy = current_position
output_index = 0

delete_item = []
vacuum_item = ["AbyssMage","AmethystLump","Crab","CrystalChunk","FatuiAgent","FatuiCicinMage","FatuiMirrorMaiden","GeovishapHatchling","Mitachurl","RawMeat","RuinDrake","RuinGuard","RuinHunter","RuinSentinel","SunsetFluit","WolvesOfTheRiht","RuinGrader","Geovishap","EyeOfTheStorm","Hilichurl","Samachurl","TreasureHoarder","Slime","Nobushi","Specter","FatuiSkirmisher","FloatingHydroFungus","TheEremites","Fowl"]
print("Deleting exclusion file...")

json_list_size = len(json_list)
for i,json_file_i in enumerate(json_list):
    if not i in delete_item:
        for j in range(i+1, json_list_size):

            ed = exclusion_distance
            if json_file_i["english"] in vacuum_item or json_list[j]["english"] in vacuum_item:
                ed = 4.5

            if (numpy.sqrt(pow(json_file_i['position'][0] - json_list[j]['position'][0],2) + pow(json_file_i['position'][2] - json_list[j]['position'][2],2)) <= ed and
                abs(json_file_i["position"][1] - json_list[j]['position'][1]) <= ed):
                delete_item.append(j)



# while len(json_list) > 0:
    
#     distance = {"value":[],"json":[]}
    
#     for json_file in json_list:
#         distance["value"].append(numpy.sqrt(pow(json_file['position'][0] - current_position[0],2) + pow(json_file['position'][2] - current_position[2],2)))
#         distance["json"].append(json_file)

#     empty_distance = False
#     while True:

#         if not distance["value"]:
#             empty_distance = True
#             break

#         nearest = min(distance["value"])
#         min_distance_index = distance["value"].index(nearest)

#         exclusion = False
#         ed = exclusion_distance

#         for vi in vacuum_item:
#             if vi in distance["json"][min_distance_index]["filename"]:
#                 ed = 4.5
#                 break
        
#         if nearest <= ed and abs(distance["json"][min_distance_index]["position"][1] - current_position[1]) <= ed:
#             exclusion = True

#         if exclusion:
#             delete_item.append(distance["json"][min_distance_index]["filename"])
#             del distance["value"][min_distance_index]
#             del distance["json"][min_distance_index]
#         else:
#             break

#     if empty_distance:
#         break

#     current_position = distance["json"][min_distance_index]['position']

#     del distance["json"][min_distance_index]
#     json_list = distance["json"]

#     output_index  = output_index + 1
print("Done")

# json_list = json_list_copy

# for index, json_data in enumerate(json_list):
#     for di in delete_item:
#         if di == json_data["filename"]:
#             del json_list[index]
#             break

json_list = json_list_copy
for i,di in enumerate(delete_item):
    del json_list[di-i]

# json_list = json_list_copy
# print(delete_item)
# for di in delete_item:
#     print(di)
#     json_list[di] = "del"

# for i,jl in enumerate(json_list):
#     if jl == "del":
#         del json_list[i]

current_position = current_position_copy
output_index = 0

while len(json_list) > 0:

    distance = {"value":[],"json":[]}
    
    for json_file in json_list:
        distance["value"].append(numpy.sqrt(pow(json_file['position'][0] - current_position[0],2) + pow(json_file['position'][2] - current_position[2],2)))
        distance["json"].append(json_file)

    distance_cond = [d for d in distance["value"] if d >= loading_distance]
    if distance_cond:
        nearest = min(distance_cond)
    else:
        nearest = min(distance["value"])
    min_distance_index = distance["value"].index(nearest)

    name = str(output_index) + "_" + distance["json"][min_distance_index]["filename"].replace("/","_").replace("\\","_").replace(".json","")

    output_json = dict()
    output_json['description'] = distance["json"][min_distance_index]['description']
    output_json['name'] = name
    output_json['position'] = distance["json"][min_distance_index]['position']

    print(name)
    #1109
    #1158

    with open(copy_dir_name + name + ".json", mode='wt', encoding='utf-8') as file:
        json.dump(output_json, file, ensure_ascii=False)

    del distance["json"][min_distance_index]
    json_list = distance["json"]

    current_position = output_json['position']

    output_index  = output_index + 1