import webbrowser
import csv
import os
import shutil
import pathlib
import datetime
from FantraxUtils.Team import Team
from FantraxUtils.Player import Player
from UpdateTeamSheets.src.sheets_connect import SheetsService

_LEAGUE_ID = 'btbtpg55kwidi85g'
statusIndex = 4

def build_team(fileName, teamName, teamId):      
    team = Team(teamName, teamId)
    keys = []
    with open(fileName, newline='') as csvfile:
        teamReader = csv.reader(csvfile, delimiter=',')
        for row in teamReader:  
            if  (len(row) == 0) or (row[0] == 'Hitting') or (row[0] == 'Pitching') or (row[0] == 'Totals'):
                # We don't care about these rows
                continue
            elif row[0] == 'Pos':
                keys = row
            else:
                p = Player(zip(keys, row))
                team.append(Player(zip(keys, row)))
        
    return team
        
def find_previous_monday_period(currentDate):
    currentDate = datetime.date.today()
    loopDay = currentDate.weekday()
    print(loopDay)
    while loopDay != 0:
        currentDate = currentDate - datetime.timedelta(days=1)
        loopDay = currentDate.weekday()
    
    # The start date of the league is actually the 28th, but we need a 1-based index for the URL string
    # so we can get that by "starting" one day early
    period = currentDate - datetime.date(year=2019,month=3,day=27)
    return period.days

def download_roster_file(period, teamId, leagueId='1jaul1j8k2v9r9j3'):
    # TODO generate season code (currently 139 for 2022 projections)
    url = 'https://www.fantrax.com/fxpa/downloadTeamRosterStats?leagueId=' + \
        leagueId + '&pageNumber=1&period=1&scoringPeriod=1&seasonOrProjection=PROJECTION_0_139_SEASON&timeframeTypeCode=YEAR_TO_DATE&scoringCategoryType=5&statsType=1&view=STATS&teamId=' + teamId + '&adminMode=false&startDate=2020-03-26&endDate=2020-09-28&lineupChangeSystem=EASY_CLICK&daily=false&origDaily=false&'
    webbrowser.get('windows-default').open(url)
    
    dwnld_directory = os.path.join(pathlib.Path.home(), 'Rosters')
    exists = False
    while exists is False:
        exists = os.path.isfile(os.path.join(dwnld_directory, 'Fantrax-Team-Roster-Millennial Bark.csv'))

    destination_file = os.path.join(os.getcwd(), 'Downloads\Fantrax-Team-Roster-Millennial Bark-' + teamId + '-' + str(period) + '.csv')
    shutil.move(os.path.join(dwnld_directory, 'Fantrax-Team-Roster-Millennial Bark.csv'), destination_file)
    return destination_file
    
def get_team_name_id_pairs(fileName):
    teamNamesIdsList = []
    keys = []
    with open(fileName, newline='') as csvfile:
        teamReader = csv.reader(csvfile, delimiter=',')
        for row in teamReader:  
            teamNamesIdsList.append((row[0], row[1]))

    return teamNamesIdsList
    
def download_teams_to_sheets():
    sheets_service = SheetsService()
    id = sheets_service.create_worksheet('SteveSheet')
    print('ID: {}'.format(id))

def main():
    # might like to make this print to a log
    print('Starting fantrax monitor...')

    download_teams_to_sheets()

    # teamsList = []
    # nameIdPairs = get_team_name_id_pairs('cfg/Teams.csv')
    # startDate = datetime.date.today()
    # currentPeriod = find_previous_monday_period(startDate)
    # startDate = datetime.date.today() - datetime.timedelta(days=7)
    # previousPeriod = find_previous_monday_period(startDate)
    # for pair in nameIdPairs:
    #     # print(pair[0] + ', ' + pair[1])
    #     if pair[0] ==  'Team Name':
    #         continue
            
    #     destination_file = download_roster_file(currentPeriod, pair[1], _LEAGUE_ID)
    #     # destination_file = download_roster_file(currentPeriod, 'gds3fwcakwidi85h', _LEAGUE_ID)
    #     teamsList.append(build_team(destination_file, pair[0], pair[1]))
    
    # for team in teamsList:
    #     keylist = list(team[0].keys())
    #     team.CheckRules()
        
if __name__ == '__main__':
    main()