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

tsfile = open('data/treatise_structure_dict.json', 'r')
tsdict = json.load(tsfile)

awprev_df = pd.read_csv('data/awpreverse.csv', index_col=0)
awcrev_df = pd.read_csv('data/awcreverse.csv', index_col=0)
swprev_df = pd.read_csv('data/swpreverse.csv', index_col=0)
swcrev_df = pd.read_csv('data/swcreverse.csv', index_col=0)

l_a_w_p = pd.read_csv('data/csvs/lit_a_w_p.csv', index_col=0)
l_a_w_c = pd.read_csv('data/csvs/lit_a_w_c.csv', index_col=0)
l_s_w_p = pd.read_csv('data/csvs/lit_s_w_p.csv', index_col=0)
l_s_w_c = pd.read_csv('data/csvs/lit_s_w_c.csv', index_col=0)
