"""
This will generate a csv with every March Madness result from 2003 and the KenPom stats of those teams
"""
from datetime import datetime
from sportsipy.ncaab.boxscore import Boxscores
import csv

name_mapping = {
    'Ohio St.':'Ohio State',
    'UC Santa Barbara':'UCSB',
    'Miami FL':'Miami (FL)',
    'Oklahoma St.':'Oklahoma State',
    'Kent St.':'Kent State',
    'UC Irvine':'UC-Irvine',
    'Connecticut':'UConn',
    'Illinois Chicago':'UIC',
    'Mississippi St.':'Mississippi State',
    'McNeese St.':'McNeese State',
    'Murray St.':'Murray State',
    'Pittsburgh':'Pitt',
    'San Diego St.':'San Diego State',
    'N.C. State':'NC State',
    'Michigan St.':'Michigan State',
    'Mississippi':'Ole Miss',
    'St. John\'s':'St. John\'s (NY)',
    'Saint Joseph\'s':'St. Joseph\'s',
    'South Carolina St.':'South Carolina State',
    'Utah St.':'Utah State',
    'Colorado St.':'Colorado State',
    'Arizona St.':'Arizona State',
    'Weber St.':'Weber State',
    'Sam Houston St.':'Sam Houston State',
    'East Tennessee St.':'ETSU',
    'Iowa St.':'Iowa State',
    'Alabama St.':'Alabama State',
    'UAB':'Alabama-Birmingham',
    'Delaware St.':'Delaware State',
    'North Carolina':'UNC',
    'Cal St. Fullerton':'Cal State Fullerton',
    'Wichita St.':'Wichita State',
    'Albany':'Albany (NY)',
    'Northwestern St.':'Northwestern State',
    'Florida St.':'Florida State',
    'Missouri St.':'Missouri State',
    'Washington St.':'Washington State',
    'Wright St.':'Wright State',
    'Massachusetts':'UMass',
    'Jackson St.':'Jackson State',
    'Texas A&M Corpus Chris':'Texas A&M-Corpus Christi',
    'Miami OH':'Miami (OH)',
    'New Mexico St.':'New Mexico State',
    'Long Beach St.':'Long Beach State',
    'Portland St.':'Portland State',
    'Mississippi Valley St.':'Mississippi Valley State',
    'Kansas St.':'Kansas State',
    'UT Arlington':'Texas-Arlington',
    'Boise St.':'Boise State',
    'Cal St. Northridge':'Cal State Northridge',
    'Morgan St.':'Morgan State',
    'Penn St.':'Penn State',
    'Morehead St.':'Morehead State',
    'North Dakota St.':'North Dakota State',
    'Cleveland St.':'Cleveland State',
    'Arkansas Pine Bluff':'Arkansas-Pine Bluff',
    'LIU Brooklyn':'LIU',
    'Saint Peter\'s':'St. Peter\'s',
    'Indiana St.':'Indiana State',
    'Loyola MD':'Loyola (MD)',
    'South Dakota St.':'South Dakota State',
    'Georgia St.':'Georgia State',
    'Fresno St.':'Fresno State',
    'Arkansas Little Rock':'Little Rock',
    'Cal St. Bakersfield':'Cal State Bakersfield',
    'Oregon St.':'Oregon State',
    'UC-Davis':'UC Davis',
    'Jacksonville St.':'Jacksonville State',
    'Loyola Chicago':'Loyola (IL)',
    'Gardner Webb':'Gardner-Webb',
    'Appalachian St.':'Appalachian State',
    'Norfolk St.':'Norfolk State'
}

def team_to_game_info(game_info, year, tag):
    teamHeading = tag + '_name'
    teamName = game[teamHeading]
    teamNameInTeamInfo = team_info[year].get(teamName, None) != None
    teamNameInNameMapping = team_info[year].get(teamName, None) == None and name_mapping_reversed.get(teamName, None) != None
    teamExists = teamNameInTeamInfo or teamNameInNameMapping
    if year == 2003 and teamName == 'Troy':
        teamExists = True
    if teamExists:
        if teamNameInNameMapping:
            teamAltName = name_mapping_reversed[teamName]
            teamName = teamAltName
        

        inMarchMadness = team_info[year].get(teamName,None) != None
        if inMarchMadness:
            game_info[teamHeading] = teamName
            game_info[teamHeading+'_Seed'] = team_info[year][teamName]['Seed']
            game_info[teamHeading+'_Win_Percentage'] = team_info[year][teamName]['Win %']
            game_info[teamHeading+'_AdjEM'] = team_info[year][teamName]['AdjEM']
            game_info[teamHeading+'_AdjO'] = team_info[year][teamName]['AdjO']
            game_info[teamHeading+'_AdjD'] = team_info[year][teamName]['AdjD']
            game_info[teamHeading+'_AdjT'] = team_info[year][teamName]['AdjT']
            game_info[teamHeading+'_Luck'] = team_info[year][teamName]['Luck']
            game_info[teamHeading+'_AdjEM_SOS'] = team_info[year][teamName]['AdjEM_SOS']
            game_info[teamHeading+'_OppO'] = team_info[year][teamName]['OppO']
            game_info[teamHeading+'_OppD'] = team_info[year][teamName]['OppD']
            game_info[teamHeading+'_AdjEM_NCSOS'] = team_info[year][teamName]['AdjEM_NCSOS']
    
    return game_info

if __name__ == "__main__":
    name_mapping_reversed = {v:k for k,v in name_mapping.items()}
    name_mapping_reversed
    team_info = {}
    with open('final_data.csv', newline='') as final_data:
        reader = csv.DictReader(final_data)
        for row in reader:
            year = int(row['Year'])
            if team_info.get(year,None) == None:
                team_info[year] = {}
            team = row['Team']
            seed = int(row['Seed'])
            win_percentage = float(row['Win %'])
            adjEM = float(row['AdjEM'])
            adjO = float(row['AdjO'])
            adjD = float(row['AdjD'])
            adjT = float(row['AdjT'])
            luck = float(row['Luck'])
            adjEM_SOS = float(row['AdjEM_SOS'])
            oppO = float(row['OppO'])
            oppD = float(row['OppD'])
            adjEM_NCSOS = float(row['AdjEM_NCSOS'])
            team_info[year][team] = {
                'Seed':seed,
                'Win %':win_percentage,
                'AdjEM':adjEM,
                'AdjO':adjO,
                'AdjD':adjD,
                'AdjT':adjT,
                'Luck':luck,
                'AdjEM_SOS':adjEM_SOS,
                'OppO':oppO,
                'OppD':oppD,
                'AdjEM_NCSOS':adjEM_NCSOS
            }

    game_data = {}
    for year in range(2002,2022):
        if year == 2020:
            continue
        game_data[year] = []


    dates = {
        2002:[(3,12),(4,1)],
        2003:[(3,18),(4,7)],
        2004:[(3,16),(4,5)],
        2005:[(3,15),(4,4)],
        2006:[(3,13),(4,3)],
        2007:[(3,13),(4,2)],
        2008:[(3,18),(4,7)],
        2009:[(3,17),(4,6)],
        2010:[(3,16),(4,5)],
        2011:[(3,15),(4,4)],
        2012:[(3,13),(4,2)],
        2013:[(3,19),(4,8)],
        2014:[(3,18),(4,7)],
        2015:[(3,17),(4,6)],
        2016:[(3,15),(4,4)],
        2017:[(3,14),(4,3)],
        2018:[(3,13),(4,2)],
        2019:[(3,19),(4,8)],
        2021:[(3,18),(4,5)]
    }
    for year in range(2002,2022):
        if year == 2020:
            continue
        start_date = dates[year][0][1]
        end_date = dates[year][1][1] + 1
        for march_date in range(start_date,32):
            month = 3
            day = march_date
            games_today = Boxscores(datetime(year, month, day))
            games = games_today.games['-'.join([str(month), str(day), str(year)])]
            for game in games:
                game_info = {}
                game_info = team_to_game_info(game_info, year, 'away')
                game_info = team_to_game_info(game_info, year, 'home')
                if game_info != {}:
                    winner = game['winning_name']
                    if winner == game['away_name']:
                        game_info['Win'] = 0
                    elif winner == game['home_name']:
                        game_info['Win'] = 1
                    game_data[year].append(game_info)
        for april_date in range(1,end_date):
            month = 4
            day = april_date
            games_today = Boxscores(datetime(year, month, day))
            games = games_today.games['-'.join([str(month), str(day), str(year)])]
            for game in games:
                game_info = {}
                game_info = team_to_game_info(game_info, year, games, 'away')
                game_info = team_to_game_info(game_info, year, games, 'home')
                if game_info != {}:
                    winner = game['winning_name']
                    if winner == game['away_name']:
                        game_info['Win'] = 0
                    elif winner == game['home_name']:
                        game_info['Win'] = 1
                    game_data[year].append(game_info)

    with open('training_data.csv','w',newline='') as training_data:
        fieldnames = ['Year','away_name','away_name_Seed','away_name_Win_Percentage','away_name_AdjEM',
                    'away_name_AdjO','away_name_AdjD','away_name_AdjT','away_name_Luck','away_name_AdjEM_SOS',
                    'away_name_OppO','away_name_OppD','away_name_AdjEM_NCSOS','home_name','home_name_Seed','home_name_Win_Percentage','home_name_AdjEM',
                    'home_name_AdjO','home_name_AdjD','home_name_AdjT','home_name_Luck','home_name_AdjEM_SOS',
                    'home_name_OppO','home_name_OppD','home_name_AdjEM_NCSOS','Win']
        
        writer = csv.DictWriter(training_data,fieldnames=fieldnames)
        writer.writeheader()
        for year, games in game_data.items():
            for game in games:
                row = game
                row['Year'] = year
                writer.writerow(row)



