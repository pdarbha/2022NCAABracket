"""
This script takes the 538 probabilities of each team winning in a given round
and outputs a cleaned and sorted version to be used by the model
"""
import pandas as pd
import numpy as np
import csv

data538 = pd.read_csv('fivethirtyeight_ncaa_forecasts.csv')
data538 = data538[0:68]

data538 = data538.drop(['gender','forecast_date','playin_flag','rd1_win','results_to','team_alive','team_id','team_rating','team_region','team_seed','team_slot'], axis=1)

sorted_data = np.zeros((66,6))
teams = {}
inv_teams = {}
with open('2022_data.csv', newline='') as final_data:
    reader = csv.DictReader(final_data)
    i = 0
    for row in reader:
        teams[i] = (row['Team'], row['Seed'])
        inv_teams[row['Team']] = i
        i+=1

for i,row in data538.iterrows():
    name = row['team_name']
    if not name in inv_teams:
        continue
    index = inv_teams[name]
    sorted_data[index] = row.drop(['team_name']).to_numpy()

pd.DataFrame(sorted_data).to_csv('538rounddata.csv', header=None, index=None)
