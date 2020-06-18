#load the files, just ensure these files are in the right directories
#or make sure the directory is correct

nToSdict = open("functions_and_classes/Norton to SBN Dictionary.txt", "r")
sToNdict = open("functions_and_classes/SBN to Norton Dictionary.txt", "r")

#create the dictionaries and lists
norton_to_sbn_dictionary = {}
treatise_paragraph_list = []
sbn_pages_list = []
sbn_to_norton_dictionary = {}
master_score_sheet = {}

#read from the Norton to SBN Dictionary
for line in nToSdict:
    para = line.split(" : ")[0].strip()
    treatise_paragraph_list.append(para)
    pages = line.split(" : ")[1].strip()
    page_list = pages.split(',')
    norton_to_sbn_dictionary[para] = page_list
    master_score_sheet[para] = 0

#read from the SBN to Norton Dictionary
for line in sToNdict:
    page = line.split(" : ")[0].strip()
    sbn_pages_list.append(page)
    paras = line.split(" : ")[1].strip()
    para_list = paras.split(',')
    sbn_to_norton_dictionary[page] = para_list

nToSdict.close()
sToNdict.close()
