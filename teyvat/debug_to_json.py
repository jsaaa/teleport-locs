import json
import glob
import os
import pyperclip
import io
import csv
import shutil
import datetime

#item_name_list = ["CommonChest","ExquisiteChest","PreciousChest","LuxuriousChest","Seelie","TimeTrialChallenge","CrimsonAgate","WarmingSeelie"]
#item_name_list = ["CommonChest","ExquisiteChest","PreciousChest","LuxuriousChest","Seelie","TimeTrialChallenge","Anemoculus","CrimsonAgate","WarmingSeelie","Geoculus","AbyssMage","AmethystLump","Berry","BirdEgg","Crab","CrystalChunk","FatuiAgent","FatuiCicinMage","FatuiMirrorMaiden","GeovishapHatchling","Matsutake","Mint","Mitachurl","Pine","RawMeat","RuinDrake","RuinGuard","RuinHunter","RuinSentinel","SmallLampGrass","SunsetFluit","SweetFlower","WolvesOfTheRiht","RuinGrader","Geovishap","EyeOfTheStorm","Hilichurl","Samachurl","TreasureHoarder","Slime","Nobushi","Specter","FatuiSkirmisher","Whopperflower","FloatingHydroFungus","TheEremites","Fowl","SumeruStonePile","Electroculus","ElectroSeelie","Dendroculus"]

item_name_list = []

dt_now = datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')

with open('アイテム名.csv') as f:
    reader = csv.DictReader(f)
    item_list_tmp = [row for row in reader]

backup_folder = ".backup/backup_" + dt_now
print("Start backup...")

print("Copying file...")
for i, ilt in enumerate(item_list_tmp):
    item_list_tmp[i]["object"] = ilt["object"].split("|")

    if ilt["read"] == "TRUE":
        print("\t└" + ilt["english"])
        if os.path.exists(ilt["english"] + "/"):
            shutil.copytree(ilt["english"], backup_folder + "/" + ilt["english"])
        item_name_list.append(ilt["english"])

if os.path.exists(backup_folder):
    print("Making zip file...")
    shutil.make_archive(backup_folder, format = 'zip', root_dir = backup_folder)
    shutil.rmtree(backup_folder + "/")

print("Backup done")


item_list = []
for ilt in item_list_tmp:

    for inl in item_name_list:

        if inl == ilt["english"]:
            item_list.append(ilt)
            break

        elif ilt == item_list_tmp[-1] and inl == item_name_list[-1]:

            dicttmp = ilt
            dictkeys = list(ilt.keys())
            for dk in dictkeys:
                dicttmp[dk] = ""
            dicttmp["english"] = inl
            item_list.append(dicttmp)

for i, item in enumerate(item_list):

    filename = []
    position = [[]]
    id_list = []
    numlist = [-1]

    if not os.path.exists(item["english"] + "/"):
        os.mkdir(item["english"] + "/")

    file_names = glob.glob(item["english"] + "/*.json")

    for file_name in file_names:
        filename.append(file_name)
        json_open = open(file_name, 'r')
        json_load = json.load(json_open)
        position.append(json_load['position'])
        id_list.append(str(json_load['description']).split(",")[0])
        numlist.append(int(json_load["name"]))

    item_list[i]["filename"] = filename
    item_list[i]["position"] = position
    item_list[i]["id"] = id_list
    item_list[i]["num"] = max(numlist) + 1

# for i in item_list:
#     print(i)

while True:

    print("\nWaiting for update of your clipboard...")

    csv_string = pyperclip.waitForNewPaste()

    f = io.StringIO()
    f.write(csv_string)
    f.seek(0)

    csv_reader = csv.DictReader(f)
    read_data = [row for row in csv_reader]
    f.close()

    for read_data_row in read_data:

        in_item_list = False
        for item in item_list:
            
            for obj in item["object"]:
                if obj in read_data_row["Name"]:
                    in_item_list = True
                    break

            if in_item_list:

                duplication = False
                empty_id = False

                item_id = read_data_row["Entity"]
                Position = float(read_data_row["PosX"]), float(read_data_row["PosY"]), float(read_data_row["PosZ"])

                pos_range = 0.1
                if item["english"] == "Seelie" or item["english"] == "WarmingSeelie" or item["english"] == "ElectroSeelie":
                    pos_range = 4
                else:
                    for iid in item['id']:
                        if item_id == iid:
                            
                            duplication = True
                            break

                if not duplication:

                    for index, pos in enumerate(item['position']):
                        if (pos and
                            (Position[0] >= pos[0] - pos_range and Position[0] <= pos[0] + pos_range) and
                            (Position[1] >= pos[1] - pos_range and Position[1] <= pos[1] + pos_range) and
                            (Position[2] >= pos[2] - pos_range and Position[2] <= pos[2] + pos_range)):
                            duplication = True

                            if item["id"][index-1] == "":

                                file_name = item["filename"][index-1]

                                json_open = open(file_name, 'r')
                                json_load = json.load(json_open)

                                json_load["description"] = str(read_data_row["Entity"]) + "," + read_data_row["Name"]

                                with open(file_name, mode='w+', encoding='utf-8') as file:
                                    json.dump(json_load, file, ensure_ascii=False)

                                empty_id = True

                            break

                if not duplication:

                    data_tmp = dict()
                
                    data_tmp['description'] = str(read_data_row["Entity"]) + "," + read_data_row["Name"]
                    data_tmp['name'] = str(item['num'])
                    data_tmp['position'] = Position

                    item['id'].append(read_data_row["Entity"])
                    item['position'].append(data_tmp['position'])

                    with open(item["english"] + "/" + str(item['num']) + '.json', mode='wt', encoding='utf-8') as file:
                        json.dump(data_tmp, file, ensure_ascii=False)

                    print(item["english"] + str(item['num']))

                    item['num'] = item['num'] + 1

                break
