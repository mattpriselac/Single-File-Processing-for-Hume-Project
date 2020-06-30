import pandas as pd
import json
#the directories to work with
csv_dir = 'data/csvs/'
txt_dir = 'data/txts/'
json_dir = 'data/jsons/'

from data.jsons import json_list

tsfile = open('data/treatise_structure_dict.json', 'r')
tsdict = json.load(tsfile)
