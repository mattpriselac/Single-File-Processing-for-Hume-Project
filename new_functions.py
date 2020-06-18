import re
import csv
import pandas as pd

class newPaper:
    def __init__(self, txt_file_name):
        self.name = txt_file_name
        self.nortonCites = []
        self.sbnCites = []
        self.rawParenthesesCapture = []
        self.tCites = []
        self.pageNumCites = []
        self.rawNortonScore = {}
        self.rawSbnScore = {}
        self.rawTScore = {}
        self.rawPageNumScore = {}
        self.a_l_p = {}
        self.a_w_p = {}
        self.s_l_p = {}
        self.s_w_p = {}
        self.totalStrictCites = 0
        self.totalAggressiveCites = 0
        self.s_w_c = {}
        self.s_l_c = {}
        self.a_w_c = {}
        self.a_l_c = {}
        self.biblio = {}


    def NortonSearch(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        #search pattern is
        ##        Capture Abstract cites with optional dash additions
        ##        Capture Appendix cites with optional dash additions
        ##        Capture Main body cites as follows:
        ##            Book. (capture both roman and arabic numeral versions)
        ##            Part. (capture both roman (capitalized and not) and arabic numerals)
        ##            Section (I left of the '.' here to be able to capture citations that are only Book.Part.Section with no paragraph citation)
        ##            optional .Paragraph(s with optional dash separator for a range of paragraphs
        nortonPattern = re.compile("""  Abs\.*(tract)*§*\d+([-–—,]\d{1,2})*|
                                        App\.*(endix)*§*\d+([-–—,]\d{1,2})*|
                                        ((I{1,3}|[123]))
                                        (\.([i]{1,3}|IV|[I]{1,3}|[1-4]))
                                        (\.\d{1,2})
                                        (
                                            (\.)(?=\d{1,2})
                                            \d{1,2}(?!\d)
                                            ([-–—,]\d{1,2}(?!([\d]|(\.\d))))*
                                        )*""", flags=re.X|re.I)
        #make the text of the paper accessible and generate the match objects
        text_name = 'txts/'+self.name+'.txt'
        paper_to_search = open(text_name, "r")
        text_to_search = paper_to_search.read().strip().replace(' ','')
        paper_to_search.close()
        matchObjects = nortonPattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.nortonCites.append(citationObject)
        if len(self.nortonCites) == 0:
            pass

    def SbnSearch(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
    ##        the search pattern this time is to start with SBN
    ##        then cover page numbers (I got rid of 0 as a starting point because a file happened to have a weird SBN0 followed by a long string of numbers
    ##        next I have an optional dash and comma separator that can be repeated to capture the multiple pages and ranges that get cited
    ##        this will require some cleaning because sometimes you get a random 'i' following the comma
        sbnPattern = re.compile(""" (?<!I)
                                    (SBN)
                                    ([1-9]\d+|[xvi]+|[XVI]+)
                                    ([-–—,](\d+|[xvi]+|[XVI]+))*""", re.X)
        #make the text of the paper accessible and generate the match objects
        text_name = 'txts/'+self.name+'.txt'
        paper_to_search = open(text_name, "r")
        text_to_search = paper_to_search.read().strip().replace(' ','')
        paper_to_search.close()
        matchObjects = sbnPattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.sbnCites.append(citationObject)
        if len(self.sbnCites) == 0:
            pass

    def parenthesesCapture(self):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        #This idea behind this search string is to get anything in parentheses with the following structure:
            #First, it can optionally start with either a 'T', 'THN', 'Treatise', or 'Hume'
            #Second, there can be a run of some intervening text but not a close parens or any numbers
            #Third, we get a page number citation with an optional p, p., or pp.
            #fourth, we get up to a three digit page number or range of up to 3 digit page numbers in either
                #roman or arabic numerals
            #The only thing I haven't figured out how to capture yet is a brief comment that appears in a few
            #cases where the authro says something like, 'my emphases' or 'italics mine'. I think that might
            #require a different search with a more restrictive start to the parentheses
        pattern = re.compile('\((T|THN|Treatise|Hume)*([A-Z]|[a-z]|[,.])*(p*\.{0,1}(\d{1,3}|[xvi]+|[XVI]+)([-–—,](\d+|[xvi]{1,5}|[XVI]{1,5}))*)\)')
        #make the text of the paper accessible and generate the match objects
        text_name = 'txts/'+self.name+'.txt'
        paper_to_search = open(text_name, "r")
        text_to_search = paper_to_search.read().strip().replace(' ','')
        paper_to_search.close()
        matchObjects = pattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.rawParenthesesCapture.append(citationObject)
        if len(self.rawParenthesesCapture) == 0:
            pass


    def a_l_p_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-a-l-p.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.a_l_p.items():
            csv_writer.writerow(pair)

    def a_w_p_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-a-w-p.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.a_w_p.items():
            csv_writer.writerow(pair)

    def s_l_p_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-s-l-p.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.s_l_p.items():
            csv_writer.writerow(pair)

    def s_w_p_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-s-w-p.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.s_w_p.items():
            csv_writer.writerow(pair)

    def a_l_c_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-a-l-c.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.a_l_c.items():
            csv_writer.writerow(pair)

    def a_w_c_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-a-w-c.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.a_w_c.items():
            csv_writer.writerow(pair)

    def s_l_c_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-s-l-c.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.s_l_c.items():
            csv_writer.writerow(pair)

    def s_w_c_CSV(self):
        csv_file = open('csvs/'+self.name[5:-4]+'-s-w-c.csv', 'w')
        csv_writer = csv.writer(csv_file)
        for pair in self.s_w_c.items():
            csv_writer.writerow(pair)

    def csvScoreDump(self):
        self.a_l_p_CSV()
        self.a_w_p_CSV()
        self.s_l_p_CSV()
        self.s_w_p_CSV()
        self.a_l_c_CSV()
        self.a_w_c_CSV()
        self.s_l_c_CSV()
        self.s_w_c_CSV()
        print('csvs dumped')

def processPaper(paper_obj):
    #this function take a paper object in and will fill the search lists with citations
    #First, conduct the searches
    paper_obj.NortonSearch()
    paper_obj.SbnSearch()
    paper_obj.parenthesesCapture()

    #second, set the easy .cleanedCitations
    for cite in paper_obj.nortonCites:
        cite.cleanedCitation = cite.rawCitationText
    for cite in paper_obj.sbnCites:
        cite.cleanedCitation = cite.rawCitationText[3:]

    #third, sort the parentheses
    #in the sorting, we'll do a first pass to get the citations that start with T or Hume or THN or Treatise:
    strict_check = re.compile(r'(Hume|Treatise|THN|T)(([, \-\–\—p\.]*)((?<!\d)\d{1,3}(?!\d)))+', re.I)
    num_check = re.compile(r'(([, \-\–\—p\.]*)((?<!\d)\d{1,3}(?!\d)))+', re.I)
    for cite in paper_obj.rawParenthesesCapture:
        #make the strict check:
        #I start it at the first character to ignore the open parens that
        if strict_check.match(cite.rawCitationText[1:]) != None:
            if num_check.search(cite.rawCitationText) != None:
                num_text = num_check.search(cite.rawCitationText).group().replace(' ', '')
                #remove 'p', 'P', '.' from the nubmers
                num_text = num_text.replace('p','')
                num_text = num_text.replace('P','')
                num_text = num_text.replace('.','')
                #set the cleanedCitation to the num_text
                cite.cleanedCitation = num_text
                #add the cite to the tCites
                paper_obj.tCites.append(cite)
        else:
            if num_check.search(cite.rawCitationText) != None:
                num_text = num_check.search(cite.rawCitationText).group().replace(' ', '')
                #remove 'p', 'P', '.' from the nubmers
                num_text = num_text.replace('p','')
                num_text = num_text.replace('P','')
                num_text = num_text.replace('.','')
                #set the cleanedCitation to the num_text
                cite.cleanedCitation = num_text
                #add the cite to pageNumCites, if it's more than one digit
                #because otherwise we catch too much argument numbering use
                #of parentheses:
                if len(num_text) > 1:
                    paper_obj.pageNumCites.append(cite)

    print (paper_obj.name, 'processed')

def chapterScores(para_scores):
    #this function takes in a dictionary score sheet for paragraph scores
    #and returns a dictionary score sheet for chapter scores
    chapter_scores = {}
    chapter_pattern = re.compile(r'(Abs)|(App\.)|(0)|(\d\.\d\.\d{1,2})')
    for para in para_scores.keys():
        chapter = chapter_pattern.match(para).group()
        if chapter not in chapter_scores.keys():
            chapter_scores[chapter] = 0
        chapter_scores[chapter] += para_scores[para]
    return chapter_scores

def citesToScores(cite_collection):
    #this function takes in a list of cites as you'd have in a paper object that's been processed
    #and returns a dictionary object with a count of total successful cites that were scored
    #and a scoresheet dictionary at the paragraph level
    out_sheet = {}
    successful_cites = 0
    for para in treatise_paragraph_list:
        out_sheet[para] = 0
    for cite in cite_collection:
        try:
            for pair in uP(cite.cleanedCitation):
                out_sheet[pair[0]] += pair[1]
            successful_cites += 1
        except Exception as e:
            print(cite.cleanedCitation, 'generated an error while scoring:', e)

    do = {}
    do['score_sheet'] = out_sheet
    do['total_cites'] = successful_cites

    return do

def relativeScoreCalc(score_dict):
    #this function calculates a score sheet relative to the paper object that is processed
    #ie how what percentage of the article's total cites go to a particular paragraph
    #get the total number of points awarded in the score_dict
    total_points = 0
    for entry in score_dict.keys():
        total_points += score_dict[entry]

    if total_points == 0:
        return score_dict

    else:
        #create the blank relative sheet
        relative_sheet = {}
        for para in treatise_paragraph_list:
            relative_sheet[para] = 0
        #fill in the blank relative sheet
        for para in relative_sheet.keys():
            relative_sheet[para] = 100 * score_dict[para]/total_points

        return relative_sheet

def paperScoreSetter(paper_obj):
    paper_obj.rawNortonScore = citesToScores(paper_obj.nortonCites)['score_sheet']
    paper_obj.rawSbnScore = citesToScores(paper_obj.sbnCites)['score_sheet']
    paper_obj.rawTScore = citesToScores(paper_obj.tCites)['score_sheet']
    paper_obj.rawPageNumScore = citesToScores(paper_obj.pageNumCites)['score_sheet']

    if len(paper_obj.nortonCites) > 5:
        paper_obj.s_w_p = paper_obj.rawNortonScore
        paper_obj.totalStrictCites = citesToScores(paper_obj.nortonCites)['total_cites']

    else:
        if len(paper_obj.sbnCites) > 5:
            strict_cites = paper_obj.nortonCites + paper_obj.sbnCites
            paper_obj.s_w_p = citesToScores(strict_cites)['score_sheet']
            paper_obj.totalStrictCites = citesToScores(strict_cites)['total_cites']
        else:
            strict_cites = paper_obj.nortonCites + paper_obj.sbnCites + paper_obj.tCites
            paper_obj.s_w_p = citesToScores(strict_cites)['score_sheet']
            paper_obj.totalStrictCites = citesToScores(strict_cites)['total_cites']

    agg_cites = paper_obj.nortonCites + paper_obj.sbnCites + paper_obj.tCites + paper_obj.pageNumCites
    paper_obj.totalAggressiveCites = citesToScores(agg_cites)['total_cites']
    paper_obj.a_w_p = citesToScores(agg_cites)['score_sheet']

    paper_obj.s_l_p = relativeScoreCalc(paper_obj.s_w_p)
    paper_obj.a_l_p = relativeScoreCalc(paper_obj.a_w_p)

    paper_obj.s_w_c = chapterScores(paper_obj.s_w_p)
    paper_obj.s_l_c = chapterScores(paper_obj.s_l_p)
    paper_obj.a_w_c = chapterScores(paper_obj.a_w_p)
    paper_obj.a_l_c = chapterScores(paper_obj.a_l_p)

    print('finished setting scores for', paper_obj.name)

def p_to_dict(paper):
    od = {}
    od['name'] = paper.name
    norton_cites_out = []
    for cite in paper.nortonCites:
        norton_cites_out.append(c_to_dict(cite))
    od['nortonCites'] = norton_cites_out
    sbn_cites_out = []
    for cite in paper.sbnCites:
        sbn_cites_out.append(c_to_dict(cite))
    od['sbnCites'] = sbn_cites_out
    raw_out = []
    for cite in paper.rawParenthesesCapture:
        raw_out.append(c_to_dict(cite))
    od['rawParenthesesCapture'] = raw_out
    t_out = []
    for cite in paper.tCites:
        t_out.append(c_to_dict(cite))
    od['tCites'] = t_out
    pageNumOut = []
    for cite in paper.pageNumCites:
        pageNumOut.append(c_to_dict(cite))
    od['pageNumCites'] = pageNumOut
    od['rawNortonScore'] = paper.rawNortonScore
    od['rawSbnScore'] = paper.rawSbnScore
    od['rawTScore'] = paper.rawTScore
    od['rawPageNumScore'] = paper.rawPageNumScore
    od['a_l_p'] = paper.a_l_p
    od['a_w_p'] = paper.a_w_p
    od['s_l_p'] = paper.s_l_p
    od['s_w_p'] = paper.s_w_p
    od['totalStrictCites'] = paper.totalStrictCites
    od['totalAggressiveCites'] = paper.totalAggressiveCites
    od['s_w_c'] = paper.s_w_c
    od['s_l_c'] = paper.s_l_c
    od['a_w_c'] = paper.a_w_c
    od['a_l_c'] = paper.a_l_c
    od['biblio'] = paper.biblio

    return od

def c_to_dict(cite):
    od = {}
    od['order'] = cite.order
    od['paper'] = cite.paper
    od['startPoint'] = cite.startPoint
    od['endPoint'] = cite.endPoint
    od['rawCitationText'] = cite.rawCitationText
    od['cleanedCitation'] = cite.cleanedCitation

    return od

def p_from_dict(in_dict):
    paper = newPaper(in_dict['name'])
    for cite in in_dict['nortonCites']:
        paper.nortonCites.append(c_from_dict(cite))
    for cite in in_dict['sbnCites']:
        paper.sbnCites.append(c_from_dict(cite))
    for cite in in_dict['rawParenthesesCapture']:
        paper.rawParenthesesCapture.append(c_from_dict(cite))
    for cite in in_dict['tCites']:
        paper.tCites.append(c_from_dict(cite))
    for cite in in_dict['pageNumCites']:
        paper.pageNumCites.append(c_from_dict(cite))
    paper.rawNortonScore = in_dict['rawNortonScore']
    paper.rawSbnScore = in_dict['rawSbnScore']
    paper.rawTScore = in_dict['rawTScore']
    paper.rawPageNumScore = in_dict['rawPageNumScore']
    paper.totalStrictCites = in_dict['totalStrictCites']
    paper.totalAggressiveCites = in_dict['totalAggressiveCites']
    paper.a_l_p = in_dict['a_l_p']
    paper.a_w_p = in_dict['a_w_p']
    paper.a_l_c = in_dict['a_l_c']
    paper.a_w_c = in_dict['a_w_c']
    paper.s_l_p = in_dict['s_l_p']
    paper.s_w_p = in_dict['s_w_p']
    paper.s_l_c = in_dict['s_l_c']
    paper.s_w_c = in_dict['s_w_c']
    paper.biblio = in_dict['biblio']

    return paper

def c_from_dict(in_dict):
    cite = Citation(in_dict['paper'], in_dict['order'], in_dict['rawCitationText'])
    cite.startPoint = in_dict['startPoint']
    cite.endPoint = in_dict['endPoint']
    cite.cleanedCitation = in_dict['cleanedCitation']

    return cite

def biblioGenerator(filename, data_frame):
    filename_filter = data_frame['Filename'].str.contains(filename)
    df_row = data_frame[filename_filter]
    do = {}
    do['Author'] = df_row['Author'].values[0]
    do['Title of Work'] = df_row['Title of Work'].values[0]
    do['Journal'] = df_row['Journal'].values[0]
    do['Volume'] = df_row['Volume'].values[0]
    do['Issue'] = df_row['Issue'].values[0]
    do['Pages'] = df_row['Pages'].values[0]
    do['Year'] = df_row['Year'].values[0]
    do['Book Title'] = df_row['Book Title'].values[0]

    return do

def biblioSetter(paper_obj, data_frame):
    paper_obj.biblio = biblioGenerator(paper_obj.name, data_frame)

def final_single_process(filename, data_frame):
    paper = newPaper(filename)
    processPaper(paper)
    paperScoreSetter(paper)
    biblioSetter(paper, data_frame)

    return paper
