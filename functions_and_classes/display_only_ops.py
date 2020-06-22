import os
import pandas as pd
from functions_and_classes.classes import *

#note: When I do this with Firestore, I think the easier way to do this will be to go through the paper object to access
#the relevant score sheet dictionary as it's saved there and load the dictionary and then load teh data frame from
#the dictinoary direclty.
def generateListOfCites(filename, a_s="a", c_p="c", w_l="w"):
    basedir = ""
    basepath = basedir+"data/csvs/"+filename
    if a_s == "a":
        if c_p == "c":
            if w_l == "w":
                path = basepath+"-a-w-c.csv"
            elif w_l == 'l':
                path = basepath+'-a-l-c.csv'
        elif c_p == 'p':
            if w_l == "w":
                path = basepath+"-a-w-p.csv"
            elif w_l == 'l':
                path = basepath+'-a-l-p.csv'
    elif a_s == "s":
        if c_p == "c":
            if w_l == "w":
                path = basepath+"-s-w-c.csv"
            elif w_l == 'l':
                path = basepath+'-s-l-c.csv'
        elif c_p == 'p':
            if w_l == "w":
                path = basepath+"-s-w-p.csv"
            elif w_l == 'l':
                path = basepath+'-s-l-p.csv'
    df = pd.read_csv(path, names=['Location', 'Count'])
    nz = df['Count'] > 0
    scdf = df[nz].sort_values('Count', ascending=False)
    entries = scdf['Location'].count()
    out_list = []
    for i in range(0,entries):
        pair = (scdf.iloc[i]['Location'], round(scdf.iloc[i]['Count'],3))
        out_list.append(pair)
    return out_list
