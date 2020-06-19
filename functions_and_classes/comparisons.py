import pandas as pd
import json
from data import csv_dir, json_dir
from data.csvs import csv_list
from data.jsons import json_list

def df_col_similarity(df, colx, coly):
    total_diff = 0
    for para in df.index:
        total_diff += abs(df[colx][para] - df[coly][para])
    return total_diff


#goal is to create a csv with comparative data
s_l_p = pd.read_csv(csv_dir+'lit_s_l_p.csv', index_col=0, header=0, names=['Literature'])
a_l_p = pd.read_csv(csv_dir+'lit_a_l_p.csv', index_col=0, header=0, names=['Literature'])
s_l_c = pd.read_csv(csv_dir+'lit_s_l_c.csv', index_col=0, header=0, names=['Literature'])
a_l_c = pd.read_csv(csv_dir+'lit_a_l_c.csv', index_col=0, header=0, names=['Literature'])

#generate a df that pairs names of files with total cites of both strict and aggressive
strict_cite_count = {}
agg_cite_count = {}
for file in json_list:
    fp = json_dir+file
    jfile = open(fp, 'r')
    jd = json.load(jfile)
    strict_cite_count[jd['name']] = jd['totalStrictCites']
    agg_cite_count[jd['name']] = jd['totalAggressiveCites']
scc_df = pd.DataFrame.from_dict(strict_cite_count, orient='index', columns=['totalStrictCites'])
agg_df = pd.DataFrame.from_dict(agg_cite_count, orient='index', columns=['totalAggressiveCites'])
total_strict_cites = scc_df['totalStrictCites'].sum()
total_agg_cites = agg_df['totalAggressiveCites'].sum()
lit_scc = pd.DataFrame([total_strict_cites], index=['Literature'], columns=['totalStrictCites'])
#this pairs strict cite count with file names
scc_df = scc_df.append(lit_scc)
lit_agg = pd.DataFrame([total_agg_cites], index=['Literature'], columns=['totalAggressiveCites'])
#this pairs aggressive cite counts with file names
agg_df = agg_df.append(lit_agg)

#first let's work on slps
slps = []
for file in csv_list:
    if '-s-l-p.csv' in file:
        slps.append(file)
for slp in slps:
    fn = slp[:-10]
    pdf = pd.read_csv(csv_dir+slp, index_col=0, names=['Score'])
    s_l_p[fn] = pdf['Score']

def updateSLPcomps():
    s_l_p_comps = pd.DataFrame(columns=s_l_p.columns, index=s_l_p.columns)
    for column in s_l_p_comps.columns:
        for ind in s_l_p_comps.index:
            s_l_p_comps[column][ind] = df_col_similarity(s_l_p,column,ind)
    s_l_p_comps = pd.merge(s_l_p_comps, scc_df, left_index=True, right_index=True)
    s_l_p_comps.to_csv('data/s_l_p_comp.csv')
    print('Done updating s_l_p_comp.csv')

#second alps
alps = []
for file in csv_list:
    if '-a-l-p.csv' in file:
        alps.append(file)
for alp in alps:
    fn = alp[:-10]
    pdf = pd.read_csv(csv_dir+alp, index_col=0, names=['Score'])
    a_l_p[fn] = pdf['Score']

def updateALPcomps():
    a_l_p_comps = pd.DataFrame(columns=a_l_p.columns, index=a_l_p.columns)
    for column in a_l_p_comps.columns:
        for ind in a_l_p_comps.index:
            a_l_p_comps[column][ind] = df_col_similarity(a_l_p,column,ind)
    a_l_p_comps = pd.merge(a_l_p_comps, agg_df, left_index=True, right_index=True)
    a_l_p_comps.to_csv('data/a_l_p_comp.csv')
    print('Done updating a_l_p_comp.csv')



#third slcs
slcs = []
for file in csv_list:
    if '-s-l-c.csv' in file:
        slcs.append(file)
for slc in slcs:
    fn = slc[:-10]
    pdf = pd.read_csv(csv_dir+slc, index_col=0, names=['Score'])
    s_l_c[fn] = pdf['Score']
def updateSLCcomps():
    s_l_c_comps = pd.DataFrame(columns=s_l_c.columns, index=s_l_c.columns)
    for column in s_l_c_comps.columns:
        for ind in s_l_c_comps.index:
            s_l_c_comps[column][ind] = df_col_similarity(s_l_c,column,ind)
    s_l_c_comps = pd.merge(s_l_c_comps, scc_df, left_index=True, right_index=True)
    s_l_c_comps.to_csv('data/s_l_c_comp.csv')
    print('Done updating s_l_c_comp.csv')

#fourth alcs
alcs = []
for file in csv_list:
    if '-a-l-c.csv' in file:
        alcs.append(file)
for alc in alcs:
    fn = alc[:-10]
    pdf = pd.read_csv(csv_dir+alc, index_col=0, names=['Score'])
    a_l_c[fn] = pdf['Score']

def updateALCcomps():
    a_l_c_comps = pd.DataFrame(columns=a_l_c.columns, index=a_l_c.columns)
    for column in a_l_c_comps.columns:
        for ind in a_l_c_comps.index:
            a_l_c_comps[column][ind] = df_col_similarity(a_l_c,column,ind)
    a_l_c_comps = pd.merge(a_l_c_comps, agg_df, left_index=True, right_index=True)
    a_l_c_comps.to_csv('data/a_l_c_comp.csv')
    print('Done updating a_l_c_comp.csv')
