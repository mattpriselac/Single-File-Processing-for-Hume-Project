from app import app, db, basedir
from flask import render_template, url_for, redirect, flash
from app.models import Paper, Citation, p_to_dict, p_from_dict, c_to_dict, c_from_dict
from google.cloud import firestore
import pandas as pd
import json
from functions_and_classes.comparisons import article_comps as ac
from data import file_to_title_dict
from functions_and_classes.comparisons import generateCompData
from functions_and_classes.display_only_ops import generateListOfCites


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Personal Identity in Hume's Treatise")

@app.route('/publications')
def publications():
    df_sc = ac('Literature', p_or_c='c', a_or_s='s')
    sc_data = generateCompData(df_sc, 'Literature')
    df_sp = ac('Literature', p_or_c='p', a_or_s='s')
    sp_data = generateCompData(df_sp, 'Literature')
    df_ac = ac('Literature', p_or_c='c', a_or_s='a')
    ac_data = generateCompData(df_ac, 'Literature')
    df_ap = ac('Literature', p_or_c='p', a_or_s='a')
    ap_data = generateCompData(df_ap, 'Literature')
    return render_template('publications.html', title="List of Publications Processed", sc=sc_data, sp=sp_data, ac=ac_data, ap=ap_data)

@app.route('/publication/<identifier>')
def publication(identifier):
    if identifier == "Literature":
        return redirect('literature')
    else:
        #try:
        pub_path =  basedir+'/data/jsons/'+identifier+'.json'
        jfile = open(pub_path, 'r')
        pub = p_from_dict(json.load(jfile))
        jfile.close()
        ppurl="https://philpapers.org/rec/"+identifier
        df_sc = ac(identifier, min_num_cites=10, min_num_comps=10, p_or_c='c', a_or_s='s')
        sc_data = generateCompData(df_sc, identifier)
        df_sp = ac(identifier, min_num_cites=10, min_num_comps=10, p_or_c='p', a_or_s='s')
        sp_data = generateCompData(df_sp, identifier)
        df_ac = ac(identifier, min_num_cites=10, min_num_comps=10, p_or_c='c', a_or_s='a')
        ac_data = generateCompData(df_ac, identifier)
        df_ap = ac(identifier, min_num_cites=10, min_num_comps=10, p_or_c='p', a_or_s='a')
        ap_data = generateCompData(df_ap, identifier)

        swp = generateListOfCites(identifier, a_s="s", c_p="p")
        swc = generateListOfCites(identifier, a_s="s", c_p="c")
        awp = generateListOfCites(identifier, a_s="a", c_p="p")
        awc = generateListOfCites(identifier, a_s="a", c_p="c")

        return render_template('publication.html', pub=pub, title=pub.name, ppurl=ppurl, sc=sc_data, sp=sp_data, ac=ac_data, ap=ap_data, swp=swp, swc=swc, awp=awp, awc=awc)

        #except:
            #return render_template('no_such_file.html', title="Whoops!", filename=identifier)

@app.route('/literature')
def literature():
    return render_template('literature.html', title="Overview of the Personal Identity Literature")

@app.route('/project')
def project():
    return render_template('project.html', title="Overview of the Project")
