import os
import json
import csv
from data import json_dir
import pandas as pd
from data.jsons import json_list
from data.txts import txt_list
from functions_and_classes.treatise_reference_data import treatise_paragraph_list
from functions_and_classes.paper_processing import process_and_score_paper as psp
from functions_and_classes.paper_processing import chapterScores, relativeScoreCalc
from functions_and_classes.paper_io import p_from_dict, p_to_dict, c_from_dict, c_to_dict

#generate the literature level scores from scratch by processing text files
def lit_scores_from_txts():
    #create the list of paragraphs to serve as the score sheet
    master_strict_para_list = {}
    for para in treatise_paragraph_list:
        master_strict_para_list[para] = 0
    #create the list of chapter to serve as the c
    master_strict_chap_list = chapterScores(master_strict_para_list)

    master_agg_para_list = {}
    for para in treatise_paragraph_list:
        master_agg_para_list[para] = 0
    #create the list of chapter to serve as the c
    master_agg_chap_list = chapterScores(master_agg_para_list)

    #now loop over the text files:
    for txt_file in txt_list:
        paper = psp(txt_file[:-4])
        for para in master_strict_para_list.keys():
                master_strict_para_list[para] += paper.s_w_p[para]
        for chapter in master_strict_chap_list.keys():
                master_strict_chap_list[chapter] += paper.s_w_c[chapter]
        if paper.totalStrictCites < 1:
                print(txt_file, 'has no strict cites')
        for para in master_agg_para_list.keys():
                master_agg_para_list[para] += paper.a_w_p[para]
        for chapter in master_agg_chap_list.keys():
                master_strict_chap_list[chapter] += paper.a_w_c[chapter]
        if paper.totalAggressiveCites < 1:
                print(txt_file, 'has no aggressive cites')

    lit_s_l_p = relativeScoreCalc(master_strict_para_list)
    lit_s_l_c = chapterScores(lit_s_l_p)
    lit_a_l_p = relativeScoreCalc(master_agg_para_list)
    lit_a_l_c = chapterScores(lit_a_l_p)

    od = {'lit_s_w_p': master_strict_para_list, 'lit_s_w_c': master_strict_chap_list, 'lit_a_w_p': master_agg_para_list, 'lit_a_w_c': master_agg_chap_list, 'lit_s_l_p': lit_s_l_p, 'lit_s_l_c': lit_s_l_c, 'lit_a_l_p': lit_a_l_p, 'lit_a_l_c': lit_a_l_c}

    return od


#generate lit level scores for all 8 kinds by reading from stored JSON data
def lit_scores_from_jsons():
    #create the list of paragraphs to serve as the score sheet
    master_strict_para_list = {}
    for para in treatise_paragraph_list:
        master_strict_para_list[para] = 0
    #create the list of chapter to serve as the c

    master_agg_para_list = {}
    for para in treatise_paragraph_list:
        master_agg_para_list[para] = 0
    #create the list of chapter to serve as the c

    for jfn in json_list:
        jfile = open(json_dir+jfn, 'r')
        jd = json.load(jfile)
        paper = p_from_dict(jd)
        jfile.close()

        for para in master_strict_para_list.keys():
                master_strict_para_list[para] += paper.s_w_p[para]
        if paper.totalStrictCites < 1:
                print(jfn[:-5], 'has no strict cites')

        for para in master_agg_para_list.keys():
                master_agg_para_list[para] += paper.a_w_p[para]
        if paper.totalAggressiveCites < 1:
                print(jfn[:-5], 'has no aggressive cites')

    lit_s_w_c = chapterScores(master_strict_para_list)
    lit_a_w_c = chapterScores(master_agg_para_list)
    lit_s_l_p = relativeScoreCalc(master_strict_para_list)
    lit_s_l_c = chapterScores(lit_s_l_p)
    lit_a_l_p = relativeScoreCalc(master_agg_para_list)
    lit_a_l_c = chapterScores(lit_a_l_p)

    od = {'lit_s_w_p': master_strict_para_list, 'lit_s_w_c': lit_s_w_c, 'lit_a_w_p': master_agg_para_list, 'lit_a_w_c': lit_a_w_c, 'lit_s_l_p': lit_s_l_p, 'lit_s_l_c': lit_s_l_c, 'lit_a_l_p': lit_a_l_p, 'lit_a_l_c': lit_a_l_c}

    return od

def pd_to_csv(dictionary, filename):
    file = open('data/csvs/'+filename+'.csv', 'w')
    csv_writer = csv.writer(file)
    csv_writer.writerow(('Paragraph','Score'))
    for item in dictionary.items():
        csv_writer.writerow(item)
    file.close()

def cd_to_csv(dictionary, filename):
    file = open('data/csvs/'+filename+'.csv', 'w')
    csv_writer = csv.writer(file)
    csv_writer.writerow(('Chapter','Score'))
    for item in dictionary.items():
        csv_writer.writerow(item)
    file.close()

def lit_to_csv(dict_of_dicts):
    for dname in dict_of_dicts.keys():
        if 'p' in dname:
            pd_to_csv(dict_of_dicts[dname], dname)
            print('generated csv for', dname)
        elif 'c' in dname:
            cd_to_csv(dict_of_dicts[dname], dname)
            print('generated csv for', dname)
