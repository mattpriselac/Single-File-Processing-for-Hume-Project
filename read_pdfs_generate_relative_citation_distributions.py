from single_file_processing_functions import extract_data_from_pdf
from treatise_reference_data import treatise_paragraph_list
import os
import csv


#generate master score sheet
print('Generating Master Score Sheet')
new_master_score_sheet = {}

for para in treatise_paragraph_list:
    new_master_score_sheet[para] = 0

cite_count_list = []

for pdf in os.listdir('pdfs'):
    print('Processing', pdf)
    if '.pdf' in pdf:
        try:
            #the data variable is the output of the extract data function, which returns
            #a dictionary and uptades files.
            #the dictionary has values for the RawCitationData, RelativeCitationData, and the
            #number of total citations found in the article.
            data = extract_data_from_pdf('pdfs/'+pdf)
            print('Updating Master Score Sheet from', pdf)
            cite_count_list.append((pdf[:-4],data['TotalCites']))
            #here we'll update the master score sheet to aggregate all the citation data
            for key in data['RawCitationData'].keys():
                new_master_score_sheet[key] += data['RawCitationData'][key]
            print('Done with', pdf)
        except Exception as e:
            print(e)

#export the list of citation counts:
cite_count_file = open('cite_counts.csv', 'w')
count_writer = csv.writer(cite_count_file)
for pair in cite_count_list:
    count_writer.writerow(pair)
cite_count_file.close()


#now we'll save a csv with raw citation data
raw_total_outfile = open('RawTotalCites.csv', 'w')
raw_writer = csv.writer(raw_total_outfile)
for pair in new_master_score_sheet.items():
    raw_writer.writerow(pair)
raw_total_outfile.close()

#now we'll work on creating a relative score sheet for the aggregated citation data
#first, we need to calculate the total number of citations
total_cite_points = 0
for pair in new_master_score_sheet.items():
    #get the paragraph, point pairs, add the point total
    total_cite_points += pair[1]
print('There were', str(total_cite_points), 'cites found')

#second we'll save a csv with the relative citation data
relative_total_outfile = open('RelativeTotalCites.csv', 'w')
relative_writer = csv.writer(relative_total_outfile)
for pair in new_master_score_sheet.items():
    para = pair[0]
    relative_score = 100 * round(pair[1]/total_cite_points, 5)
    new_pair = (para, relative_score)
    relative_writer.writerow(new_pair)
relative_total_outfile.close()


print('There were', str(total_cite_points), 'cites found')
print('We tried to search', str(len(os.listdir('pdfs'))), 'pdfs')
print("We couldn't extract anything from", str(len(os.listdir('pdfs'))-len(os.listdir(('txts')))), "of them")
print('We produced', str(len(os.listdir('csvs'))), 'csv files with relative citation frequency scores')
