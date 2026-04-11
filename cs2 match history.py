import pandas as pd
from pathlib import Path
import datetime as dt

base_dir = Path(__file__).resolve().parent #gets dir of python file
file_path = base_dir / "match_history.csv"                                

# csmatches_df = pd.DataFrame(columns=[                           # COMMENT OUT THIS LINE AFTER YOU RUN FOR THE FIRST EVER TIME 
#     "Match Type", 
#     "Average Ping", 
#     "Kills",
#     "Deaths",
#     "Assists",
#     "MVPs",
#     "HSP",
#     "Score",
#     "Outcome",
#     "Map Score",
#     "Map",
#     "Time",
#     "Date",
#     "Day",
#     "Played with"
# ])

csmatches_df = pd.read_csv(file_path)                  # UNCOMMENT THIS LINE AND COMMENT OUT THE INITIALIZING DF SET UP AFTER THE FIRST TIME 
csmatches_df = csmatches_df.loc[:, ~csmatches_df.columns.str.startswith('Unnamed')] # removes index collums


with open(base_dir / "match_result_input.txt" ) as infile:
    game_data = infile.read().splitlines()

# get the players user name for finding their stat line
ign = "gambling helpline"
#ign = input("What is your username? ")
user_index = -1

#for line in game_data:                #GETTING DATA FROM INPUT FILE 🔥🔥🔥🔥🔥
#    print(line)
 
match_type = game_data[0].rsplit()[0]               # prem or comp
map = ""

map = (" ".join(game_data[0].rsplit()[1:]))                    # map played



for i, line in enumerate(game_data):
    if line == ign:
        user_index = i + 1

statline = game_data[user_index].rsplit()      #users main stats from the game

ping = statline[0]                  # players ping
kills = statline[1]                 # players kills
assists = statline[2]                # players assists
deaths = statline[3]                # players deaths
score = statline[-1]                # players total score in game 
head_shot_percent = statline[-2]    # players hsp for game

mvps = 0
mvp_string = list(statline[4])
num_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

if "˜" in mvp_string and str(mvp_string[-1]) in num_list:         #since ~ is only used in mvp stat we can look for that
    mvps = mvp_string[-1]
elif "˜" in mvp_string and str(mvp_string[-1]) not in num_list:
    mvps = 1
else: 
    pass

map_score = game_data[24]                            # hid map score here too hehe
if user_index < 24:                                  # hard coded to line 26 so copy and paste has to be same everytime, find the users position relative to this line
    team = 1
else:
    team = 2

scores = map_score.rsplit()
if int(scores[0]) > int(scores[-1]):
    winner = 1
else:
    winner = 2

if winner == team:                                 # outcome of the match
    outcome = "Win"
else:
    outcome = "Loss"

date_and_time = game_data[1].rsplit()               # get date time the game was played NOT changed to nzt

gmt_datetime = dt.datetime.strptime(f"{date_and_time[0]} {date_and_time[1]}", "%Y-%m-%d %H:%M:%S")  # proper formatting 

nz_datetime = gmt_datetime + dt.timedelta(hours=12)

date = nz_datetime.date()
time = nz_datetime.strftime("%#I:%M %p")
day = nz_datetime.strftime("%A")

solo = ""

while solo not in ["Y", "N"]:
    solo = input("Did you solo queue? (Y/N) ")
    if solo not in ["Y", "N"]:  
        print("Invalid Answer")
    else:
        break

team_mates_list = []
n_team_mates = -1

if solo == 'N':
    while int(n_team_mates) not in [1, 2, 3, 4]:
        n_team_mates = input("How many people did you stack with? ")
        if int(n_team_mates) not in [1, 2, 3, 4]:
            print("Invalid Answer please try again")

    for i in range(int(n_team_mates)):
        friend = input("Name ONE: ")
        team_mates_list.append(friend)

team_mates = (", ".join(team_mates_list))


# ADDING IT ALL TO THE DF

csmatches_df.loc[len(csmatches_df)] = {
    "Match Type": match_type,
    "Average Ping": ping,
    "Kills": kills,
    "Deaths": deaths,
    "Assists": assists,
    "MVPs": mvps,
    "HSP": head_shot_percent,
    "Score": score,
    "Outcome": outcome,
    "Map Score": map_score,
    "Map": map,
    "Time": time,
    "Date": date,
    "Day": day,
    "Played with": team_mates
}

# print()

print(csmatches_df)
csmatches_df.to_csv(file_path, index=False)