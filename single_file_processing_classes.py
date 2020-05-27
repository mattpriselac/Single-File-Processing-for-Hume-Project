import re
import roman
import os
import csv
from treatise_reference_data import *
from master_function_list import ultimateParser as uP

class Paper:
    def __init__(self, txt_file_name):
        self.name = txt_file_name
        self.nortonCites = []
        self.sbnCites = []
        self.rawParenthesesCapture = []
        self.otherCites = []

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
        nortonPattern = re.compile("""  T*Abs\d+
                                            ([-–—]\d{1,2}){0,1}|
                                        T*App\d+
                                            ([-–—]\d{1,2}){0,1}|
                                        ((I{1,3}|[123])\.)
                                        (([i]{1,3}|IV|[I]{1,3}|[1-4])\.)
                                        (\d{1,2})
                                        (\.[1-9]\d{0,2}
                                            ([-–—]\d{1,2}){0,1}
                                        ){0,1}""", re.X)
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.name, "r")
        text_to_search = paper_to_search.readline()
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
        paper_to_search = open(self.name, "r")
        text_to_search = paper_to_search.readline()
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
        paper_to_search = open(self.name, "r")
        text_to_search = paper_to_search.readline()
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

    def otherSearch(self, search_term):
        citationCounter = 0 #citation counter to be used in numbering citations
        #create the citation search object
        pattern = re.compile(search_term)
        #make the text of the paper accessible and generate the match objects
        paper_to_search = open(self.name, "r")
        text_to_search = paper_to_search.readline()
        paper_to_search.close()
        matchObjects = pattern.finditer(text_to_search)
        #create a citation for each match object
        for match in matchObjects:
            citationCounter +=1
            citationObject = Citation(self.name, citationCounter, match.group())
            citationObject.startPoint = match.start()
            citationObject.endPoint = match.end()
            citationObject.search_term = match.re
            self.otherCites.append(citationObject)
        if len(self.otherCites) == 0:
            pass

    def calculate_raw_score_sheet(self):
        #gather all the citations
        master_citation_list = []
        for citation in self.nortonCites:
            master_citation_list.append(citation)
        for citation in self.sbnCites:
            master_citation_list.append(citation)
        for citation in self.rawParenthesesCapture:
            master_citation_list.append(citation)
        for citation in self.otherCites:
            master_citation_list.append(citation)

        #turn each citation into a list of pairs
        master_scoring_list = []
        for citation in master_citation_list:
            if citation.cleanedCitation != "":
                try:
                    for pair in uP(citation.cleanedCitation):
                        #these pairs are (chapter, weight)
                        master_scoring_list.append(pair)
                except Exception as e:
                    print(e)
                    print(pair, "generated an error calculating raw_score_sheet while running through uP")
                    pass

        #create a blank scoring sheet:
        score_sheet = {}
        for para in treatise_paragraph_list:
            score_sheet[para] = 0

        #update score_sheet from master_score list
        for pair in master_scoring_list:
            try:
                score_sheet[pair[0]] += pair[1]
            except Exception as error:
                print(error)
                print(pair[0], 'generated a key error when trying to update the score sheet')
                pass

        return score_sheet

    def make_csv_raw_score(self):
        out_data = self.calculate_raw_score_sheet()
        output_file = open('csvs/'+self.name[5:-4]+".csv", "w")
        csv_writer = csv.writer(output_file)
        for pair in out_data.items():
            csv_writer.writerow(pair)
        output_file.close()
        print('raw score sheet csv generated')

    def relative_score_sheet(self):
        raw_score = self.calculate_raw_score_sheet()
        total_score = 0
        for para in raw_score.keys():
            if raw_score[para] > 0:
                total_score += raw_score[para]
        relative_score_sheet = {}
        for para in raw_score.keys():
            if raw_score[para] > 0:
                relative_score = 100*round(raw_score[para]/total_score,5)
                relative_score_sheet[para] = relative_score
            else:
                relative_score_sheet[para] = raw_score[para]

        return relative_score_sheet

    def make_csv_relative_score(self):
        out_data = self.relative_score_sheet()
        output_file = open('csvs/'+self.name[5:-4]+"-relative-score.csv", "w")
        csv_writer = csv.writer(output_file)
        for pair in out_data.items():
            csv_writer.writerow(pair)
        output_file.close()
        print('relative score sheet csv generated')

class Citation:
    def __init__(self, paper_name, order_num, search_result):
        self.order = order_num
        self.paper = paper_name
        self.search_term = ""
        self.citationScores = []
        self.startPoint = 0
        self.endPoint = 0
        self.rawCitationText = search_result
        self.precedingText = ""
        self.trailingText = ""
        self.cleanedCitation = ""

    #this function pulls a given number of characters from before the citation starts up to the start
    #of the citation
    def FindPrecedingText(self, num_chars):
        #open the paper file
        paper_file = open(self.paper, "r")
        text_to_use = paper_file.readline()
        paper_file.close()
        #generate the buffer to get the appropriate slice in case it's around an edge of teh string
        buffer = self.startPoint - num_chars
        #set the proper text in the Citation
        if self.startPoint == 0:
            self.precedingText = ''
        elif buffer >= 0:
            self.precedingText = text_to_use[buffer:self.startPoint]
        elif buffer < 0:
            self.precedingText[:self.startPoint]

    #this function pulls a given number of characters from the end of the citation going forward
    def FindTrailingText(self, num_chars):
        #open the paper file
        paper_file = open(self.paper, "r")
        text_to_use = paper_file.readline()
        paper_file.close()
        #generate the buffer to get the appropriate slice in case it's around an edge of the string
        buffer = len(text_to_use) - (self.endPoint + num_chars)
        #set the proper text in the Citation
        if buffer == 0:
            self.trailingText = ""
        elif buffer > 0:
            self.trailingText = text_to_use[self.endPoint:(self.endPoint + num_chars)]
        elif buffer < 0:
            self.trailingText = text_to_use[self.endPoint:]

    #this function takes an integer as input and runs the previous two functions
    def PopulateSurroundingTexts(self, num_chars):
        self.FindPrecedingText(num_chars)
        self.FindTrailingText(num_chars)

    def parensCleaner(self):
        num_check = re.compile('(\d{1,3})+([-–—,](\d{1,3}))*')
        p_cite_check = re.compile('(p{0,2}\.)*\d{1,3}')
        only_num = get_num = re.compile('\d+')
        #first, get cites that only have 'T'
        if self.rawCitationText[1] == "T":
            #now make sure we only have a after the T
            if num_check.search(self.rawCitationText) != None:
                pageNum = num_check.search(self.rawCitationText).group()
                self.cleanedCitation = pageNum

        #disabling this for now as it's probably too aggressive in polluting
        #i think the safer way to use it is as something with particular journal like Hume Studies
        #now get cites that start with a p or pp. or just a number
        elif p_cite_check.search(self.rawCitationText) != None:
            #get rid of the single digits that are often part of laying out structure of an argument
            if len(p_cite_check.search(self.rawCitationText).group()) > 1:
                #get the numbers only from the results of the page number group of the intiial re search
                num_only = only_num.search(p_cite_check.search(self.rawCitationText).group()).group()
                self.cleanedCitation = num_only
