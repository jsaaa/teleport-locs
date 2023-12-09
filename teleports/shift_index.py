import os
import json

def load_json_files(folder_path):
    json_list = []
    
    # 指定したフォルダ内のファイルを取得
    file_list = os.listdir(folder_path)
    
    # ファイルごとに処理
    for file_name in file_list:
        # ファイルのパスを作成
        file_path = os.path.join(folder_path, file_name)
        
        # ファイルがJSON形式であるかを確認
        if file_name.endswith('.json'):
            # JSONファイルを読み込み、リストに追加
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                json_list.append(data)
    
    return json_list

output_folder_path = 'output'  # 出力フォルダパスを指定
input_folder_path = '聖遺物1、エリート、鉱石'  # 読み込みフォルダパスを指定
json_data = load_json_files(input_folder_path)  # JSONファイルを読み込む

shift = 101  #ずらす数
# 読み込んだJSONデータの表示
for data in json_data:
    splited_name = data['name'].split('_')
    idx = int(splited_name[0]) + shift
    splited_name[0] = str(idx)
    shifted_name = '_'.join(splited_name)
    data['name'] = shifted_name

    print(shifted_name)
    with open(output_folder_path + '/' + shifted_name + '.json', 'w') as file:
        json.dump(data, file)