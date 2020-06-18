import os
json_list = []
path = 'data/jsons/'
raw_list = os.listdir(path)
for file in raw_list:
    if '.json' in file:
        json_list.append(file)

json_list
