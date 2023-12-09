import matplotlib.pyplot
import numpy
import glob
import json

path = "全て/"

file_names = glob.glob(path + "*.json")

x = []
y = []
for file_name in file_names:
    json_open = open(file_name, 'r')
    json_load = json.load(json_open)
    x.append(json_load["position"][0])
    y.append(json_load["position"][2])

# プロット
matplotlib.pyplot.plot(x, y, label="test",marker=".",ls="")

# 凡例の表示
matplotlib.pyplot.legend()

# プロット表示(設定の反映)
matplotlib.pyplot.show()