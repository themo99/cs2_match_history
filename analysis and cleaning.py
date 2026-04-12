import pandas as pd
from pathlib import Path
import datetime as dt
import matplotlib.pyplot as plt

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

def outcome_to_binary(df, col):
    """turns the win/loss outcome into binary for analysis"""
    df[col] = df[col].map({'Win': 1, 'Loss': 0})
    return df

#print(csmatches_df)

#analysis stuff :)))

total_kills = sum(csmatches_df['Kills'])
total_deaths = sum(csmatches_df['Deaths'])
alltime_kd = round(total_kills/total_deaths,2)
games_played = len(csmatches_df)
kills_per_game = round(total_kills/games_played, 2)

print(f"In {games_played} games you have {total_kills} kills. This is {kills_per_game} kills a game!") # output info on wr, etc.
print(f"You have died {total_deaths} times. This gives you a K/D of {alltime_kd}.")

# maps_played = csmatches_df['Map'].value_counts()                      # how many times each map has been played
# print(maps_played)

outcome_to_binary(csmatches_df, 'Outcome')                 # change outcome to binary

map_groups = csmatches_df.groupby('Map').agg(
    total_kills=('Kills', 'sum'),
    total_deaths=('Deaths', 'sum'),
    total_plays=('Map', 'count'),  
)

victories_df = csmatches_df[csmatches_df['Outcome'] == 1]

victory_map_groups = victories_df.groupby('Map').agg(
    total_wins=('Map', 'count')
)

full_df = pd.merge(map_groups, victory_map_groups, on='Map', how='left')            
full_df = full_df.fillna(0)

kd_per_map = (full_df['total_kills'] / full_df['total_deaths'])
wr_per_map = (full_df['total_wins'] / full_df['total_plays'])


print(kd_per_map)
#print(map_groups['total_wins'])

print(full_df, wr_per_map)
# csmatches_df.plot(x='Kills', y='HSP')
# plt.show()



#csmatches_df.to_csv(file_path, index=False)
