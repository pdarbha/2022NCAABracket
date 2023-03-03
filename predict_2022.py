"""
Based on trained KenPom or 538 data, generate a set of predictions that leads to the greatest
expected score.
The score for a bracket is equal to sum((is_correct ? 1 : 0) * seed * round_multiplier)
"""
from math import exp
import pandas as pd
import numpy as np
import csv

probabilities = pd.read_csv('probabilities_2022.csv',header=None).to_numpy()

teams = {}
inv_teams = {}
with open('2022_data.csv', newline='') as final_data:
    reader = csv.DictReader(final_data)
    i = 0
    for row in reader:
        teams[i] = (row['Team'], row['Seed'])
        inv_teams[row['Team']] = i
        i+=1

contenders = [
    'Gonzaga','Georgia St.',
    'Boise St.','Memphis',
    'Connecticut','New Mexico St.',
    'Arkansas','Vermont',
    'Alabama','Rutgers',
    'Texas Tech','Montana St.',
    'Michigan St.','Davidson',
    'Duke','Cal St. Fullerton',
    'Baylor','Norfolk St.',
    'North Carolina','Marquette',
    'Saint Mary\'s','Indiana',
    'UCLA','Akron',
    'Texas','Virginia Tech',
    'Purdue','Yale',
    'Murray St.','San Francisco',
    'Kentucky','Saint Peter\'s',
    'Arizona','Bryant',
    'Seton Hall','TCU',
    'Houston','UAB',
    'Illinois','Chattanooga',
    'Colorado St.','Michigan',
    'Tennessee','Longwood',
    'Ohio St.','Loyola Chicago',
    'Villanova','Delaware',
    'Kansas','Texas Southern',
    'San Diego St.','Creighton',
    'Iowa','Richmond',
    'Providence','South Dakota St.',
    'LSU','Iowa St.',
    'Wisconsin','Colgate',
    'USC','Miami FL',
    'Auburn', 'Jacksonville St.'
]
rounds = []
round = 0
round_mults = [1,2,4,8,16,32]
expected_score = 0


"""
Greedy Version
For each game, which ever team gives the most expected points for that result advances
Drawback: this doesn't take acount expected points lost in further rounds by eliminating a team
"""
def greedy_algorithm():
    while len(contenders) > 1:
        rounds.append(contenders)
        advanced = []
        i = 0
        while i < len(contenders):
            team_a,team_b = contenders[i],contenders[i+1]
            index_a,index_b = inv_teams[team_a],inv_teams[team_b]
            p = probabilities[index_a,index_b]
            if p == 0:
                p = 1.0 - probabilities[index_b,index_a]
            seed_a,seed_b = float(teams[index_a][1]),float(teams[index_b][1])
            ev_a,ev_b = round_mults[round]*seed_a*p,round_mults[round]*seed_b*(1-p)
            if ev_a > ev_b:
                advanced.append(team_a)
                expected_score += (ev_a - ev_b)
            else:
                advanced.append(team_b)
                expected_score += (ev_b - ev_a)
            i+=2
        contenders = advanced
        round+=1
    print("=======GREEDY ALGORITHM==========")
    print(contenders)
    print(expected_score)
    print(rounds)
    print("==================================")

"""
[['Gonzaga', 'Georgia St.', 'Boise St.', 'Memphis', 'Connecticut', 'New Mexico St.', 'Arkansas', 'Vermont', 'Alabama', 'Rutgers', 'Texas Tech', 'Montana St.', 'Michigan St.', 'Davidson', 'Duke', 'Cal St. Fullerton', 'Baylor', 'Norfolk St.', 'North Carolina', 'Marquette', "Saint Mary's", 'Indiana', 'UCLA', 'Akron', 'Texas', 'Virginia Tech', 'Purdue', 'Yale', 'Murray St.', 'San Francisco', 'Kentucky', "Saint Peter's", 'Arizona', 'Bryant', 'Seton Hall', 'TCU', 'Houston', 'UAB', 'Illinois', 'Chattanooga', 'Colorado St.', 'Michigan', 'Tennessee', 'Longwood', 'Ohio St.', 'Loyola Chicago', 'Villanova', 'Delaware', 'Kansas', 'Texas Southern', 'San Diego St.', 'Creighton', 'Iowa', 'Richmond', 'Providence', 'South Dakota St.', 'LSU', 'Iowa St.', 'Wisconsin', 'Colgate', 'USC', 'Miami FL', 'Auburn', 'Jacksonville St.'], 
['Gonzaga', 'Boise St.', 'Connecticut', 'Vermont', 'Alabama', 'Texas Tech', 'Davidson', 'Duke', 'Baylor', 'Marquette', 'Indiana', 'UCLA', 'Virginia Tech', 'Purdue', 'San Francisco', 'Kentucky', 'Arizona', 'Seton Hall', 'Houston', 'Illinois', 'Michigan', 'Tennessee', 'Loyola Chicago', 'Villanova', 'Kansas', 'Creighton', 'Iowa', 'South Dakota St.', 'Iowa St.', 'Wisconsin', 'Miami FL', 'Auburn'], 
['Boise St.', 'Connecticut', 'Alabama', 'Davidson', 'Marquette', 'Indiana', 'Virginia Tech', 'San Francisco', 'Seton Hall', 'Houston', 'Michigan', 'Loyola Chicago', 'Creighton', 'Iowa', 'Iowa St.', 'Miami FL'], 
['Boise St.', 'Alabama', 'Marquette', 'Virginia Tech', 'Houston', 'Michigan', 'Iowa', 'Iowa St.'], 
['Boise St.', 'Virginia Tech', 'Houston', 'Iowa St.'], 
['Virginia Tech', 'Houston'],
['Houston']]
score: 187.27
"""


"""
A more dynamic approach, which takes into consideration future value lost using 538 round by round data
"""
def dynamic_538():
    data538 = pd.read_csv('538rounddata.csv',header=None).to_numpy()
    E = np.zeros((66,7))
    for i in range(66):
        seed = teams[i][1]
        E[i,5] = 32 * float(seed) * data538[i][5]
        for j in range(4,-1,-1):
            mult = round_mults[j]
            E[i,j] = mult * float(seed) * data538[i,j] + E[i,j+1]

    while len(contenders) > 1:
        rounds.append(contenders)
        advanced = []
        i = 0
        while i < len(contenders):
            team_a,team_b = contenders[i],contenders[i+1]
            index_a,index_b = inv_teams[team_a],inv_teams[team_b]
            p = probabilities[index_a,index_b]
            if p == 0:
                p = 1.0 - probabilities[index_b,index_a]
            seed_a,seed_b = float(teams[index_a][1]),float(teams[index_b][1])
            ev_a,ev_b = round_mults[round]*seed_a*p,round_mults[round]*seed_b*(1-p)
            if ev_a + E[index_a,round+1] > ev_b + E[index_b,round+1]:
                advanced.append(team_a)
                expected_score += (ev_a - ev_b)
            else:
                advanced.append(team_b)
                expected_score += (ev_b - ev_a)
            i+=2
        contenders = advanced
        round+=1
    print("=======DYNAMIC ALGORITHM WITH 538==========")
    print(contenders)
    print(expected_score)
    print(rounds)
    print("================================8==========")

"""
['Houston']
115.80059233869837
[['Gonzaga', 'Georgia St.', 'Boise St.', 'Memphis', 'Connecticut', 'New Mexico St.', 'Arkansas', 'Vermont', 'Alabama', 'Rutgers', 'Texas Tech', 'Montana St.', 'Michigan St.', 'Davidson', 'Duke', 'Cal St. Fullerton', 'Baylor', 'Norfolk St.', 'North Carolina', 'Marquette', "Saint Mary's", 'Indiana', 'UCLA', 'Akron', 'Texas', 'Virginia Tech', 'Purdue', 'Yale', 'Murray St.', 'San Francisco', 'Kentucky', "Saint Peter's", 'Arizona', 'Bryant', 'Seton Hall', 'TCU', 'Houston', 'UAB', 'Illinois', 'Chattanooga', 'Colorado St.', 'Michigan', 'Tennessee', 'Longwood', 'Ohio St.', 'Loyola Chicago', 'Villanova', 'Delaware', 'Kansas', 'Texas Southern', 'San Diego St.', 'Creighton', 'Iowa', 'Richmond', 'Providence', 'South Dakota St.', 'LSU', 'Iowa St.', 'Wisconsin', 'Colgate', 'USC', 'Miami FL', 'Auburn', 'Jacksonville St.'], 
['Gonzaga', 'Memphis', 'Connecticut', 'Arkansas', 'Alabama', 'Texas Tech', 'Davidson', 'Duke', 'Baylor', 'North Carolina', 'Indiana', 'UCLA', 'Virginia Tech', 'Purdue', 'San Francisco', 'Kentucky', 'Arizona', 'TCU', 'Houston', 'Illinois', 'Michigan', 'Tennessee', 'Loyola Chicago', 'Villanova', 'Kansas', 'San Diego St.', 'Iowa', 'South Dakota St.', 'LSU', 'Wisconsin', 'Miami FL', 'Auburn'], 
['Gonzaga', 'Connecticut', 'Texas Tech', 'Duke', 'North Carolina', 'UCLA', 'Purdue', 'Kentucky', 'Arizona', 'Houston', 'Tennessee', 'Villanova', 'Kansas', 'Iowa', 'LSU', 'Auburn'], 
['Gonzaga', 'Texas Tech', 'UCLA', 'Kentucky', 'Houston', 'Tennessee', 'Iowa', 'LSU'], 
['Gonzaga', 'UCLA', 'Houston', 'Iowa'], 
['UCLA', 'Houston']]
['Houston']
score = 115.80059233869837
"""

"""
TODO: Dynamic Programming using trained probabilities
"""

if __name__ == "__main__":
    greedy_algorithm()
    dynamic_538()
