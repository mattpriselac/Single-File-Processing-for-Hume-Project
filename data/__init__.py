import pandas as pd
#the directories to work with
csv_dir = 'data/csvs/'
txt_dir = 'data/txts/'
json_dir = 'data/jsons/'

a_l_c_comp = pd.read_csv('data/a_l_c_comp.csv', index_col=0)
a_l_p_comp = pd.read_csv('data/a_l_p_comp.csv', index_col=0)
s_l_c_comp = pd.read_csv('data/s_l_c_comp.csv', index_col=0)
s_l_p_comp = pd.read_csv('data/s_l_p_comp.csv', index_col=0)
