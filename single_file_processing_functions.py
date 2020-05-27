import re
import roman
import os
import csv
from treatise_reference_data import *
from master_function_list import ultimateParser as uP
from single_file_processing_classes import *
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def extractCitationDataFromSinglePaper(file_in):
    #generate the paper object
    paper_obj = Paper('txts/'+file_in)

    #conduct the searches
    paper_obj.NortonSearch()
    paper_obj.SbnSearch()
    paper_obj.parenthesesCapture()

    #create counter for cleaned parens
    clean_parens_counter = 0
    
    #clean the citations
    for citation in paper_obj.nortonCites:
        citation.cleanedCitation = citation.rawCitationText
    for citation in paper_obj.sbnCites:
        citation.cleanedCitation = citation.rawCitationText[3:]
    for citation in paper_obj.rawParenthesesCapture:
        citation.parensCleaner()
        if citation.cleanedCitation != '':
            clean_parens_counter += 1
            

    

    
        
    #generate the raw citation data for the paper:
    raw_score_sheet = paper_obj.calculate_raw_score_sheet()

    #generate the relative citation data for the paper:
    relative_score_sheet = paper_obj.relative_score_sheet()

    #output the csv of relative citation
    paper_obj.make_csv_relative_score()

    #create the output dictionary
    od = {
        'TotalCites': len(paper_obj.nortonCites)+len(paper_obj.sbnCites)+clean_parens_counter,
        'RelativeCitationData': relative_score_sheet,
        'RawCitationData': raw_score_sheet
    }

    #return the output dictionary
    return od

def convert_pdf_to_no_ws_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()

    file_name = path.split('/')[len(path.split('/'))-1][:-4]+".txt"
    output_file = open("txts/"+file_name, 'w')

    for line in text:
        outline = line.replace(" ", "")
        output_file.write(outline.strip())

    output_file.close()

    print('Created No WS txt at', 'txts/'+file_name)

    return(file_name)


def extract_data_from_pdf(pdf_file_input_path):
    #takes a path to a pdf file and returns a dictionary and generates a relative score csv
    #the dictionary is 'TotalCites': INT of number of cites in paper
    # 'RelativeCitationData': relative_score_sheet,
    #  'RawCitationData': raw_score_sheet
    # each of those score sheets is a dictionary with keys of paragraphs and values of citation data.
    # relative citation data is the percentage of citations, raw is just the count

    txt_conversion_path = convert_pdf_to_no_ws_txt(pdf_file_input_path)
    scoring_dict = extractCitationDataFromSinglePaper(txt_conversion_path)

    return scoring_dict
