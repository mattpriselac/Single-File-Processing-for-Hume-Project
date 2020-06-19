import pandas as pd
import json
from data import csv_dir, json_dir
from data.csvs import csv_list
from data.jsons import json_list
from data import a_l_p_comp, a_l_c_comp, s_l_p_comp, s_l_c_comp
#This file has two categories of thigns worth importing for usage:
#first is a function for generating comparisons:
#article_comps(filename, min_num_cites=1, min_num_comps=100, a_or_s="a", p_or_c="p")
#Second are the comparative data frame updaters:
#updateALCcomps, updateALPcomps, updateSLCcomps, updateSLPcomps
#those will update the a_l_p_comp csvs and when the data module is reloaded it will
#draw the new data frames.

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


#now that we've finished the functions for generating and saving data I'll add functions for generating comparative data for an individual article

def n_agg_filter(df_in, num):
    return df_in['totalAggressiveCites'] > num

def m_agg_similar(filename, min_cites, min_similar, df_in):
    min_cit = max(0,min_cites)
    min_c = n_agg_filter(df_in, min_cit)
    min_si = min(min_similar,len(df_in[min_c].index)-1)
    sim_score_to_beat = 1.05 * df_in[min_c].sort_values(filename)[min_si:min_si+1][filename].values[0]
    score_to_beat_filter = df_in[min_c][filename] <= sim_score_to_beat

    return df_in[min_c][score_to_beat_filter].sort_values(filename)

def a_l_c_comp_process(file, minimum_comp_cites, minimum_sim_comps):
    df = pd.merge(a_l_c_comp[file], a_l_c_comp['totalAggressiveCites'], left_index=True, right_index=True)
    return m_agg_similar(file, minimum_comp_cites, minimum_sim_comps, df)[1:]

def a_l_p_comp_process(file, minimum_comp_cites, minimum_sim_comps):
    df = pd.merge(a_l_p_comp[file], a_l_p_comp['totalAggressiveCites'], left_index=True, right_index=True)
    return m_agg_similar(file, minimum_comp_cites, minimum_sim_comps, df)[1:]

def n_strict_filter(df_in, num):
    return df_in['totalStrictCites'] > num

def m_strict_similar(filename, min_cites, min_similar, df_in):
    min_cit = max(0,min_cites)
    min_c = n_strict_filter(df_in, min_cit)
    min_si = min(min_similar,len(df_in[min_c].index)-1)
    sim_score_to_beat = 1.05 * df_in[min_c].sort_values(filename)[min_si:min_si+1][filename].values[0]
    score_to_beat_filter = df_in[min_c][filename] <= sim_score_to_beat

    return df_in[min_c][score_to_beat_filter].sort_values(filename)

def s_l_c_comp_process(file, minimum_comp_cites, minimum_sim_comps):
    df = pd.merge(s_l_c_comp[file], s_l_c_comp['totalStrictCites'], left_index=True, right_index=True)
    return m_strict_similar(file, minimum_comp_cites, minimum_sim_comps, df)[1:]

def s_l_p_comp_process(file, minimum_comp_cites, minimum_sim_comps):
    df = pd.merge(s_l_p_comp[file], s_l_p_comp['totalStrictCites'], left_index=True, right_index=True)
    return m_strict_similar(file, minimum_comp_cites, minimum_sim_comps, df)[1:]

#this is in the end all that needs to be imported from this file to generate the comparative data for an individaul file, along with the a_l_p_comp etc dfs from data
def article_comps(filename, min_num_cites=1, min_num_comps=100, a_or_s="a", p_or_c="p"):
    if a_or_s == "a":
        if p_or_c == "p":
            return a_l_p_comp_process(filename, minimum_comp_cites=min_num_cites, minimum_sim_comps=min_num_comps)
        elif p_or_c == "c":
            return a_l_c_comp_process(filename, minimum_comp_cites=min_num_cites, minimum_sim_comps=min_num_comps)
        else:
            return print('be sure to choose "p" or "c" for the p_or_c argument')
    elif a_or_s == "s":
        if p_or_c == "p":
            return s_l_p_comp_process(filename, minimum_comp_cites=min_num_cites, minimum_sim_comps=min_num_comps)
        elif p_or_c == "c":
            return s_l_c_comp_process(filename, minimum_comp_cites=min_num_cites, minimum_sim_comps=min_num_comps)
        else:
            return print('be sure to choose "p" or "c" for the p_or_c argument')
    else:
        return print('be sure to choose "a" or "s" for the a_or_s argument')
