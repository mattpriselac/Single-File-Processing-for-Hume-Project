#generates the data frame with bibio info.
import pandas as pd

refs = pd.read_csv('data/List-of-Works.csv', header=0)
na_in_dl = refs['Downloaded?'].notna()
na_in_dl
dl_no_na = refs[na_in_dl]
dl_yes = dl_no_na['Downloaded?'].str.contains('yes', case=False)
dl_files = dl_no_na[dl_yes]
dl_files
