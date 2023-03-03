"""
Scraping KenPom for custom stats of each team for training (2002-2021)
and testing (2022)
"""
import requests
from bs4 import BeautifulSoup
import csv

"""
scrapes kenpom.com for tournament teams and their stats from 2002-2021
outputs training data to final_data.csv
"""
def scrape_training_data():
    team_data = {}
    tourney_teams = {}
    for year in range(2002, 2022):
        URL = 'https://kenpom.com/index.php?y='+str(year)
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        tourney_teams[year] = {}
        team_data[year] = {}
        rows = soup.findAll('tr')
        for row in rows:
            if row.attrs.get('class') and ('thead1' in row.attrs.get('class') or 'thead2' in row.attrs.get('class')):
                continue
            span = row.find('td', {'class':'next_left'}).find('span', {'class':'seed'})
            if span:
                name = row.find('td', {'class':'next_left'}).find('a').text
                seed = row.find('td', {'class':'next_left'}).find('span', {'class':'seed'}).text
                tourney_teams[year][name]=seed
                values = row.contents
                team_name = values[2].contents[0].contents[0]
                record = values[4].text.split('-')
                win = float(record[0])/(float(record[0])+float(record[1]))
                adjEM = float(values[5].contents[0])
                adjO = float(values[6].contents[0])
                adjD = float(values[8].contents[0])
                adjT = float(values[10].contents[0])
                luck = float(values[12].contents[0])
                adjEM_SOS = float(values[14].contents[0])
                oppO = float(values[16].contents[0])
                oppD = float(values[18].contents[0])
                adjEM_NCSOS = float(values[20].contents[0])
                team_data[year][team_name] = {
                    'Year': year,
                    'Team': name,
                    'Seed': seed,
                    'Win %': win,
                    'AdjEM': adjEM,
                    'AdjO': adjO,
                    'AdjD': adjD,
                    'AdjT': adjT,
                    'Luck': luck,
                    'AdjEM_SOS': adjEM_SOS,
                    'OppO': oppO,
                    'OppD': oppD,
                    'AdjEM_NCSOS': adjEM_NCSOS
                }
    with open('final_data.csv', 'w', newline='') as final_data:
        fieldnames = ['Year', 'Team', 'Seed', 'Win %', 'AdjEM', 'AdjO', 'AdjD', 'AdjT', 'Luck', 'AdjEM_SOS', 'OppO', 'OppD', 'AdjEM_NCSOS']
        writer = csv.DictWriter(final_data, fieldnames=fieldnames)
        writer.writeheader()
        for year, teams in team_data.items():
            # there was no tournament in 2020
            if year == 2020:
                continue
            for team in teams:
                row = team_data[year][team]
                writer.writerow(row)


"""
scrapes kenpom.com for tournament teams and their stats in 2022
outputs training data to 2022_data.csv
"""
def scrape_test_data():
    URL = 'https://kenpom.com/index.php?y=2022'
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    rows = soup.find_all('tr', {'class':'tourney'})
    teams_2022 = {}
    for row in rows:
        name = row.find('td', {'class':'next_left'}).find('a').text
        seed = row.find('td', {'class':'next_left'}).find('span', {'class':'seed'}).text
        values = row.contents
        team_name = values[2].contents[0].contents[0]
        record = values[4].text.split('-')
        win = float(record[0])/(float(record[0])+float(record[1]))
        adjEM = float(values[5].contents[0])
        adjO = float(values[6].contents[0])
        adjD = float(values[8].contents[0])
        adjT = float(values[10].contents[0])
        luck = float(values[12].contents[0])
        adjEM_SOS = float(values[14].contents[0])
        oppO = float(values[16].contents[0])
        oppD = float(values[18].contents[0])
        adjEM_NCSOS = float(values[20].contents[0])
        teams_2022[team_name] = {
            'Year': 2022,
            'Team': name,
            'Seed': seed,
            'Win %': win,
            'AdjEM': adjEM,
            'AdjO': adjO,
            'AdjD': adjD,
            'AdjT': adjT,
            'Luck': luck,
            'AdjEM_SOS': adjEM_SOS,
            'OppO': oppO,
            'OppD': oppD,
            'AdjEM_NCSOS': adjEM_NCSOS
        }
    with open('2022_data.csv', 'w', newline='') as final_data:
        fieldnames = ['Year', 'Team', 'Seed', 'Win %', 'AdjEM', 'AdjO', 'AdjD', 'AdjT', 'Luck', 'AdjEM_SOS', 'OppO', 'OppD', 'AdjEM_NCSOS']
        writer = csv.DictWriter(final_data, fieldnames=fieldnames)
        writer.writeheader()
        for team in teams_2022.keys():
            row = teams_2022[team]
            writer.writerow(row)

if __name__ == "__main__":
    scrape_training_data()
    scrape_test_data()
