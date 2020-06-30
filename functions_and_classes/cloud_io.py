from google.cloud import firestore
from google.cloud import storage
import pandas as pd
import json
from io import StringIO, BytesIO
from functions_and_classes.paper_io import *

#Storage up and download functions
#this function takes care of pulling a csv and generating the data frame.
#It's what I need. I'll create a function sheet for cloud storage io
def df_from_gc_csv(csv_name):
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(csv_name)
    dl_data = io.BytesIO(blob.download_as_string())
    df = pd.read_csv(dl_data, index_col=0)

    return df

##This does the same thing but for JSON objects
def dic_from_gc_json(json_name):
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(json_name)
    dl_data = io.BytesIO(blob.download_as_string())
    do = json.load(dl_data)

    return do

#Same thing but for txt files, returns a list of lines
def txt_from_gc_txt(txt_name):
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(txt_name)
    dl_data = blob.download_as_string()
    usable_string = dl_data.decode('utf-8')
    lines_split = usable_string.split('\n')

    return lines_split

#Here's a function to upload to a given file name in the bucket from a given path. It
#was used for the first upload of static docs to the cloud.
def upload_to_gc(file_name, file_path):
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(file_name)
    blob.upload_from_filename(file_path)

    print(file_name, 'uploaded to gcloud storage')

#the following two functinos write directly from a file to the cloud storage bucket, the first takes a
#data frame in and outputs a csv to the cloud with the file_name. The second takes a dictionary in
#and outputs a json to the cloud with the file_name.
def upload_csv_from_df(file_name, df):
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(file_name)
    file_obj = io.StringIO(df.to_csv())
    blob.upload_from_file(file_obj)
    print(file_name, 'uploaded!')

def upload_json_from_dict(file_name, dic_in):
    #enter a name for the file and the dictinoary, will upload json.
    sc = storage.Client()
    bkt = sc.bucket('treatise-mapping-project.appspot.com')
    blob = bkt.blob(file_name)
    file_obj = io.StringIO(json.dumps(dic_in))
    blob.upload_from_file(file_obj)
    print(file_name, 'uploaded!')


##From here down we have Functions for firestore database connections for paper objects:
def upload_paper_dict_to_firedb(paper_dict):
    base_line = {}
    base_line['biblio'] = paper_dict['biblio']
    base_line['name'] = paper_dict['name']
    base_line['totalAggressiveCites'] = paper_dict['totalAggressiveCites']
    base_line['totalStrictCites'] = paper_dict['totalStrictCites']
    base_line['rawNortonScore'] = paper_dict['rawNortonScore']
    base_line['rawSbnScore'] = paper_dict['rawSbnScore']
    base_line['rawTScore'] = paper_dict['rawTScore']
    base_line['rawPageNumScore'] = paper_dict['rawPageNumScore']

    #set the basic information
    basic_ref = firedb.collection(u'publications').document(paper_dict['name'])
    basic_ref.set(base_line)

    #set the cites
    cites_ref = basic_ref.collection(u'citations')
    cites = {}
    cites[('nortonCites')] = paper_dict['nortonCites']
    cites[('sbnCites')] = paper_dict['sbnCites']
    cites[('tCites')] = paper_dict['tCites']
    cites[('pageNumCites')] = paper_dict['pageNumCites']
    cites[('rawParenthesesCapture')] = paper_dict['rawParenthesesCapture']
    cites_ref.document('cites').set(cites)

    #set the scores
    scores_ref = basic_ref.collection(u'scores')
    scores_ref.document('a_l_p').set(paper_dict['a_l_p'])
    scores_ref.document('a_l_c').set(paper_dict['a_l_c'])
    scores_ref.document('a_w_p').set(paper_dict['a_w_p'])
    scores_ref.document('a_w_c').set(paper_dict['a_w_c'])
    scores_ref.document('s_l_p').set(paper_dict['s_l_p'])
    scores_ref.document('s_l_c').set(paper_dict['s_l_c'])
    scores_ref.document('s_w_p').set(paper_dict['s_w_p'])
    scores_ref.document('s_w_c').set(paper_dict['s_w_c'])

    print('done uploading', paper_dict['name'])

def p_dict_from_fire(fname):
    doc_ref = firedb.collection('publications').document(fname)
    #get and set basic info
    base_dict = doc_ref.get().to_dict()
    od = {}
    od['biblio'] = base_dict['biblio']
    od['name'] = base_dict['name']
    od['totalAggressiveCites'] = base_dict['totalAggressiveCites']
    od['totalStrictCites'] = base_dict['totalStrictCites']
    od['rawNortonScore'] = base_dict['rawNortonScore']
    od['rawSbnScore'] = base_dict['rawSbnScore']
    od['rawTScore'] = base_dict['rawTScore']
    od['rawPageNumScore'] = base_dict['rawPageNumScore']
    #get and set cites
    cites_ref = doc_ref.collection('citations').document('cites')
    cites_dict = cites_ref.get().to_dict()
    od['nortonCites'] = cites_dict['nortonCites']
    od['sbnCites'] = cites_dict['sbnCites']
    od['tCites'] = cites_dict['tCites']
    od['pageNumCites'] = cites_dict['pageNumCites']
    od['rawParenthesesCapture'] = cites_dict['rawParenthesesCapture']
    #get and set scores
    scores_ref = doc_ref.collection('scores')
    od['a_l_p'] = scores_ref.document('a_l_p').get().to_dict()
    od['a_l_c'] = scores_ref.document('a_l_c').get().to_dict()
    od['a_w_p'] = scores_ref.document('a_w_p').get().to_dict()
    od['a_w_c'] = scores_ref.document('a_w_c').get().to_dict()
    od['s_l_p'] = scores_ref.document('s_l_p').get().to_dict()
    od['s_l_c'] = scores_ref.document('s_l_c').get().to_dict()
    od['s_w_p'] = scores_ref.document('s_w_p').get().to_dict()
    od['s_w_c'] = scores_ref.document('s_w_c').get().to_dict()
    print(fname, ' recovered into a paper dict ready form')
    return od

def paper_from_fire(filename):
    d_from_fire = p_dict_from_fire(filename)
    paper = p_from_dict(d_from_fire)
    return paper

def paper_to_fire(paper_obj):
    p_dict = p_to_dict(paper_obj)
    upload_paper_dict_to_firedb(p_dict)
    print('Done uploading', paper_obj.name)
