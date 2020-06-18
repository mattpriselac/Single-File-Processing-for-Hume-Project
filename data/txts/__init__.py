import os
txt_list = []
path = 'data/txts/'
raw_list = os.listdir(path)
for file in raw_list:
    if 'txt' in file:
        txt_list.append(file)

txt_list
