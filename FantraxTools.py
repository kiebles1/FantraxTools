from UpdateTeamSheets.src.sheets_connect import SheetsService
import FantraxUtils.FantraxUtils as FantraxUtils
from FantraxUtils import Team
import datetime
import argparse
import csv

def create_arb_workbook(teamName):
    service = SheetsService()
    workbookId = service.execute_sheets_operation('create', workbook_name=teamName + '_' + str(datetime.date.today().year))
    return workbookId

def populate_team_sheet(teamName, teamId, workbookId):
    print('not ready')

def write_headers_to_team_sheet(workbookId, teamName, headers):
    service = SheetsService()
    service.execute_sheets_operation('write', worksheet_id=workbookId, sheet_name=teamName, data=[headers])

def create_arb_sheet_keys_list():
    keys_list = list()
    keys_list.append('Pos')
    keys_list.append('Player')
    keys_list.append('Team')
    keys_list.append('Eligible')
    keys_list.append('Status')
    keys_list.append('Salary')
    return keys_list

def create_arb_sheet_player_list(player):
    player_list = list()
    player_list.append(player['Pos'])
    player_list.append(player['Player'])
    player_list.append(player['Team'])
    player_list.append(player['Eligible'])
    player_list.append(player['Status'])
    player_list.append(player['Salary'])
    
    # extra fields for arb stuff, current allocation and new salary
    player_list.append(0)
    player_list.append('=INDEX(A1:G, ROW(), 6) + INDEX(A1:G, ROW(), 7)')
    return player_list

def write_player_to_team_sheet(teamName, workbookId, player):
    service = SheetsService()
    # data has to be a 2d list, even if you only have 1 row of data
    player_data = create_arb_sheet_player_list(player)
    service.execute_sheets_operation('write', worksheet_id=workbookId, sheet_name=teamName, data=[player_data])

def add_team_to_arb_workbook(teamName, teamId, workbookId):
    service = SheetsService()
    service.execute_sheets_operation('add_sheet', worksheet_id=workbookId, sheet_name=teamName)

def remove_leftover_sheet_from_arb_workbook(workbookId):
    service = SheetsService()
    service.execute_sheets_operation('delete_sheet', worksheet_id=workbookId, sheet_id=0)

def export_roster_to_arb_workbook(team, workbookId):
    keys_data = create_arb_sheet_keys_list()
    # append extra colums for arbitration to the keys list
    keys_data.append('Allocation')
    keys_data.append('New Total')
    service = SheetsService()
    service.execute_sheets_operation('write', worksheet_id=workbookId, sheet_name=team.name, data=[keys_data])
    for player in team:
        # TODO consider if there is a batch write that maybe counts as less operations
        if player['Status'] != 'Min':
            print('writing player {} from team {}'.format(player, team.name))
            write_player_to_team_sheet(team.name, workbookId, player)

def protect_arb_workbook_cells(workbookId, team):
    service = SheetsService()
    service.execute_sheets_operation('protect_range', worksheet_id=workbookId, sheet_name=team)

def apply_data_validation_to_arb_workbook(workbookId, team):
    service = SheetsService()
    service.execute_sheets_operation('apply_data_validation', worksheet_id=workbookId, sheet_name=team)

def create_arb_workbooks():
    workbookIds = dict()
    pairsList = FantraxUtils.get_team_name_id_pairs('./FantraxUtils/cfg/Teams.csv')
    for outerPair in pairsList:
        outerName = outerPair[0]
        outerId = outerPair[1]
        if outerName == 'Team Name':
            continue

        currentWorkbookId = create_arb_workbook(outerName)
        workbookIds[outerName] = currentWorkbookId

        for innerPair in pairsList:
            innerName = innerPair[0]
            innerId = innerPair[1]
            # teams don't need to do their own arb
            if (innerName == 'Team Name') or (innerName == outerName):
                continue

            add_team_to_arb_workbook(innerName, innerId, currentWorkbookId)
            protect_arb_workbook_cells(currentWorkbookId, innerName)
            apply_data_validation_to_arb_workbook(currentWorkbookId, innerName)

        remove_leftover_sheet_from_arb_workbook(currentWorkbookId)
    
    return workbookIds

def handle_args():
    parser = argparse.ArgumentParser(description='Perform different services for a Fantrax fantasy baseball league. Valid functions are "generate" and "process".')
    parser.add_argument('functions', type=str, nargs='+', help='functions to perform')
    parser.add_argument('-s', '--sheets', action='store_true', help='Write google sheets from existing rosters')
    parser.add_argument('p', '--prompt', action='store_true', help='Prompt user before saving new salary')
    args = parser.parse_args()
    if ('process' not in args.functions) and (args.prompt is True):
        print('WARNING: \'prompt\' only used when performing the \'process\' funciton. Ignoring...')
    return args

def generate_full_arb_workbooks(teamsList):
    workbookIds = create_arb_workbooks()
    for team in teamsList:
        team.workbookId = workbookIds[team.name]
        for arbTeam in teamsList:
            wbid = workbookIds[team.name]
            print('for team {} and wbid {} and arbTeam {}, starting roster export'.format(team, wbid, arbTeam))
            export_roster_to_arb_workbook(arbTeam, wbid)

def get_workbook_id_for_team(teamName):
    with open('FantraxUtils/cfg/ids.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='|')
        for row in reader:
            if row[0] == teamName:
                id = row[1]

    return id

def update_league_salaries(teamsList):
    updatedRows = list()
    with open('FantraxUtils/cfg/FantraxPlayers.csv', 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            for team in teamsList:
                player = team.GetPlayerForID(row[0])
                if player is not None:
                    updatedRows.append(row)
                    row[5] = player['Salary']
                    break

    with open('FantraxUtils/cfg/FantraxPlayers_new.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(updatedRows)

def apply_salaries(teamsList):
    update_league_salaries(teamsList)
        # for player in team:
            # input('{}: {}'.format(player['Player'], player['Salary']))

def process_arb_workbooks(teamsList, prompt=False):
    for arbTeam in teamsList:
        print('current arb: {}'.format(arbTeam.name))
        arbTeam.UpdateAllMajorsSalaries(2)
        id = get_workbook_id_for_team(arbTeam.name)
        service = SheetsService()
        runningSalary = 0
        for team in teamsList:
            runningTeamSalary = 0
            if team.name == arbTeam.name:
                continue
            salaries = service.execute_sheets_operation('read', worksheet_id=id, sheet_name=team.name, data_range='G2:G')
            playerNames = service.execute_sheets_operation('read', worksheet_id=id, sheet_name=team.name, data_range='B2:B')
            if playerNames is None:
                print('playerNames None! {}, {}'.format(arbTeam.name, team.name))
            if salaries is None:
                print('salaries None! {}, {}'.format(arbTeam.name, team.name))
            # zip only iterates as far as the shortest passed list, so if one list is longer, as 'salaries' often is because people
            # add a total to the end of the column, this still works out fine
            newSalaryList = zip(playerNames, salaries)
            for item in newSalaryList:
                if prompt is True:
                    input('enter! player item: {}'.format(item))
                team.UpdatePlayerSalary(item[0][0], int(item[1][0]))
                runningTeamSalary += int(item[1][0])
                runningSalary += int(item[1][0])

            if runningTeamSalary > 3:
                print('WARNING: {} allocated over $3 ({}) to team {}'.format(arbTeam.name, runningTeamSalary, team.name))
            elif runningTeamSalary < 1:
                print('WARNING: {} did not allocate any money ({})to {}'.format(arbTeam.name, runningTeamSalary, team.name))

        if runningSalary > 25:
            print('WARNING: {} allocated over $25 ({})'.format(arbTeam.name, runningSalary))
        elif runningSalary < 25:
            print('WARNING: {} allocated less than $25 ({})'.format(arbTeam.name, runningSalary))

    apply_salaries(teamsList)

def main():
    args = handle_args()
    print('sheets set to {}'.format(str(args.sheets)))
    teamsList = FantraxUtils.create_all_teams(sheets=args.sheets)
    if 'generate' in args.functions:
        generate_full_arb_workbooks(teamsList)
    
    if 'process' in args.functions:
        process_arb_workbooks(teamsList, args.prompt)

    for team in teamsList:
        if team.name == 'SouthSliders':
            for player in team:
                print('Player: {}\n\tSalary: {}'.format(player['Player'], player['Salary']))

if __name__ == '__main__':
    main()