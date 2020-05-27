import pandas as pd
import os

#All you need to get this script going is
#    (1) a csv file that has the relative cites for the scholarly literature
#   (2) a folder with all of the relative-score csvs for each article.

#First
#generate master data frame with that has relative citation scores for all articles.
#To start just generate the index as the paragraphs and the first column as the
#relative total citations for the body of scholarship
master_df = pd.read_csv('RelativeTotalCites.csv', index_col=0, names=['Paragraphs', 'RelativeTotalCites'])

#Second
#add a column for each article
#To do this, get a list of all articles
relative_citation_score_list = os.listdir('csvs')
#for each article's relative scores, create a column:
for file in relative_citation_score_list:
    if '.csv' in file:
        #generate a df for the article with Treatise paragraphs as index and relative citation requency as values
        article_df = pd.read_csv('csvs/'+file, index_col=0, names=['Paragraphs', file[:-19]])
        #add the column to master_df with teh article name as the column
        master_df[file[:-19]] = article_df[file[:-19]]

#Now we need to define our differential calculator to create a total differential. The goal here
#is to calculate the difference between two articles/columns for each paragraph and total those up

def df_col_diff(df, colx, coly):
    total_diff = 0
    #for each paragraph inthe Treatise
    for para in df.index:
        #get the difference between x and y, and add it to the total
        total_diff += abs(df[colx][para] - df[coly][para])
    #return the total difference between two articles.
    return total_diff

#now we can use our function to evaluate differences between articles and calculate the difference between each
#article and every other article. To do that, we need to create a data frame with a column and a row for each article
#First, create the empty data frame, which is 87x87
comparison_df = pd.DataFrame(index=master_df.columns, columns=master_df.columns)
#Second, fill it in
for article_x in master_df.columns:
    for article_y in master_df.columns:
        comparison_df[article_x][article_y] =  df_col_diff(master_df, article_x, article_y)

#now that our data frame is filled in, we can generate a csv of it to make it persist
comparison_df.to_csv('overall_similarity_scores.csv')
