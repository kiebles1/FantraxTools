import webbrowser
import csv
import os
import shutil
import pathlib
import datetime
from FantraxUtils.Team import Team
from FantraxUtils.Player import Player
from UpdateTeamSheets.src.sheets_connect import SheetsService

_LEAGUE_ID = 'wkr127m7l90hdm8n'
statusIndex = 4

def build_team(fileName, teamName, teamId):      
    print('building team {}'.format(teamName))
    team = Team(teamName, teamId)
    keys = []
    with open(fileName, newline='') as csvfile:
        teamReader = csv.reader(csvfile, delimiter=',')
        for row in teamReader:  
            if  (len(row) == 0) or (row[1] == 'Hitting') or (row[1] == 'Pitching') or (row[1] == 'Totals'):
                # We don't care about these rows
                continue
            elif row[0] == 'ID':
                keys = row
            else:
                print('keys: {}'.format(keys))
                print('row: {}'.format(row))
                team.append(Player(zip(keys, row)))
        
    return team
        
def find_previous_monday_period(currentDate):
    loopDay = currentDate.weekday()
    print(loopDay)
    while loopDay != 0:
        currentDate = currentDate - datetime.timedelta(days=1)
        loopDay = currentDate.weekday()
    
    # The start date of the league is actually the 28th, but we need a 1-based index for the URL string
    # so we can get that by "starting" one day early
    period = currentDate - datetime.date(year=2019,month=3,day=27)
    return period.days

def download_roster_file(period, teamId, leagueId=_LEAGUE_ID):
    # TODO generate season code (currently 139 for 2022 projections)
    url = 'https://www.fantrax.com/fxpa/downloadTeamRosterStats?leagueId=' + \
        leagueId + '&pageNumber=1&period=1&scoringPeriod=' + str(period) + '&seasonOrProjection=PROJECTION_0_141_SEASON&timeframeTypeCode=YEAR_TO_DATE&scoringCategoryType=5&statsType=1&view=STATS&teamId=' + teamId + '&adminMode=false&startDate=2023-03-30&endDate=2023-10-02&lineupChangeSystem=EASY_CLICK&daily=false&origDaily=false&'
    webbrowser.get('windows-default').open(url)
    
    dwnld_directory = os.path.join(pathlib.Path.home(), 'Downloads')
    exists = False
    while exists is False:
        exists = os.path.isfile(os.path.join(dwnld_directory, 'Fantrax-Team-Roster-Millennial Bark.csv'))

    destPath = os.path.join(os.getcwd(), 'Rosters')
    if os.path.isdir(destPath) == False:
        os.mkdir(destPath)

    destination_file = os.path.join(destPath, 'Fantrax-Team-Roster-Millennial Bark-' + teamId + '-' + str(period) + '.csv')
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

def get_roster_file(period, teamId):
    destPath = os.path.join(os.getcwd(), 'Rosters')
    if os.path.isdir(destPath) == False:
        os.mkdir(destPath)

    destination_file = os.path.join(destPath, 'Fantrax-Team-Roster-Millennial Bark-' + teamId + '-' + str(period) + '.csv')
    if os.path.isfile(destination_file) is True:
        return destination_file
    else:
        print("ERROR: File {} does not exist".format(destination_file))

    return None

#TODO add destination dir as param
def create_all_teams(period=None, leagueId=_LEAGUE_ID, teamsFile='./FantraxUtils/cfg/Teams.csv', sheets=False):
    teamsList = list()
    if period is None:
        nameIdPairs = get_team_name_id_pairs(teamsFile)
        for pair in nameIdPairs:
            if pair[0] == 'Team Name':
                continue
            
            if sheets is False:
                destination_file = download_roster_file(1, pair[1])
            else:
                destination_file = get_roster_file(1, pair[1])
                
            teamsList.append(build_team(destination_file, pair[0], pair[1]))

    return teamsList

#TODO add destination dir as param
def download_all_roster_files(period=None, leagueId=_LEAGUE_ID, teamsFile='cfg/Teams.csv'):
    fileList = list()
    if period is None:
        nameIdPairs = get_team_name_id_pairs(teamsFile)
        for pair in nameIdPairs:
            if pair[0] == 'Team Name':
                continue
                
            destination_file = download_roster_file(1, pair[1])
            fileList.append(destination_file)

def main():
    # might like to make this print to a log
    print('Starting fantrax monitor...')

    teamsList = create_all_teams()

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