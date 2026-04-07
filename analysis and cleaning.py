import pandas as pd
from pathlib import Path
import datetime as dt

base_dir = Path(__file__).resolve().parent #gets dir of python file
file_path = base_dir / "match_history.csv"     

csmatches_df = pd.read_csv(file_path)                  # UNCOMMENT THIS LINE AND COMMENT OUT THE INITIALIZING DF SET UP AFTER THE FIRST TIME 

# clean the played with column :))

def cleaning_lists(df, col):
    """function that gets rid of list brackets in string"""
    for i, row in csmatches_df.iterrows():
        ugly_string = row[col]
        replacement_str = ugly_string[2:-2]
        df.at[i,col] = replacement_str

#cleaning_lists(csmatches_df, 'Played with')


print(csmatches_df)



csmatches_df.to_csv(file_path, index=False)
