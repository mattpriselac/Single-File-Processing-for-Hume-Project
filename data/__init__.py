import pandas as pd
import json
#the directories to work with
csv_dir = 'data/csvs/'
txt_dir = 'data/txts/'
json_dir = 'data/jsons/'
from data.jsons import json_list


a_l_c_comp = pd.read_csv('data/a_l_c_comp.csv', index_col=0)
a_l_p_comp = pd.read_csv('data/a_l_p_comp.csv', index_col=0)
s_l_c_comp = pd.read_csv('data/s_l_c_comp.csv', index_col=0)
s_l_p_comp = pd.read_csv('data/s_l_p_comp.csv', index_col=0)

file_to_title_dict = {}
for file in json_list:
    jfile = open('data/jsons/'+file, 'r')
    jd = json.load(jfile)
    jfile.close()
    file_to_title_dict[file[:-5]] = jd['biblio']['Title of Work']
