import pandas as pd
from pathlib import Path
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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

def outcome_to_binary(df, col):
    """turns the win/loss outcome into binary for analysis"""
    df[col] = df[col].map({'Win': 1, 'Loss': 0})
    return df

def cleaning_hsp(df, col):
    """function that removes the % in hsp and changes type to int"""
    for i, row in csmatches_df.iterrows():
        ugly_string = row[col]
        replacement_str = ugly_string[:-1]
        df.at[i,col] = replacement_str
    df[col] = pd.to_numeric(df[col], errors='coerce')

#cleaning_lists(csmatches_df, 'Played with')

cleaning_hsp(csmatches_df, 'HSP')

csmatches_df['Date'] = pd.to_datetime(csmatches_df['Date'])
csmatches_df['Time'] = pd.to_datetime(csmatches_df['Time']).dt.hour * 60 + pd.to_datetime(csmatches_df['Time']).dt.minute

#analysis stuff :)))

total_kills = sum(csmatches_df['Kills'])
total_deaths = sum(csmatches_df['Deaths'])
alltime_kd = round(total_kills/total_deaths,2)
games_played = len(csmatches_df)
kills_per_game = round(total_kills/games_played, 2)

print(f"In {games_played} games you have {total_kills} kills. This is {kills_per_game} kills a game!") # output info on wr, etc.
print(f"You have died {total_deaths} times. This gives you a K/D of {alltime_kd}.")

# create a data frame for groupings by maps

outcome_to_binary(csmatches_df, 'Outcome')                 # change outcome to binary

map_groups = csmatches_df.groupby('Map').agg(
    total_kills=('Kills', 'sum'),
    total_deaths=('Deaths', 'sum'),
    total_plays=('Map', 'count'),  
)

# create a second df for grouping, this time only counting games the user won

victories_df = csmatches_df[csmatches_df['Outcome'] == 1]

victory_map_groups = victories_df.groupby('Map').agg(
    total_wins=('Map', 'count')
)

full_df = pd.merge(map_groups, victory_map_groups, on='Map', how='left')                    # merge everything     
full_df = full_df.fillna(0)

full_df['kd_per_map'] = (full_df['total_kills'] / full_df['total_deaths'])
full_df['wr_per_map'] = (round(full_df['total_wins'] / full_df['total_plays'] * 100))

#print(map_groups['total_wins'])

print(full_df)

# plot and graph generation

correlation_map = sns.heatmap(               # see how related each variable is
    csmatches_df.corr(numeric_only=True),
    annot=True, cmap="coolwarm"
)

map_list = csmatches_df['Map'].unique()                 # this block gets the amount of maps and evenly seperates each one for the colour map 
n_unique_maps = len(map_list)
colour_partions = np.linspace(0, 1, n_unique_maps)
cmap = plt.cm.get_cmap('tab10')
colour_map = {map_name: cmap(colour_partions[i]) for i, map_name in enumerate(map_list)}
colours = csmatches_df['Map'].map(colour_map)

plt.show()

plt.scatter(x=csmatches_df['Kills'],                # see how many kills i get coloured by map
            y=csmatches_df['Deaths'],
            c=colours)

for map_name, colour in colour_map.items():
    plt.scatter([], [], color=colour, label=map_name)
plt.legend()

print(csmatches_df.dtypes)
print(colour_partions)
plt.show()



#csmatches_df.to_csv(file_path, index=False)
