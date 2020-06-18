import os
csv_list = []
path = 'data/csvs/'
raw_list = os.listdir(path)
for file in raw_list:
    if '.csv' in file:
        csv_list.append(file)

csv_list
