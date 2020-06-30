import json
from data.jsons import json_list

file_to_title_dict = {}
for file in json_list:
    jfile = open('data/jsons/'+file, 'r')
    jd = json.load(jfile)
    jfile.close()
    file_to_title_dict[file[:-5]] = jd['biblio']['Title of Work']
