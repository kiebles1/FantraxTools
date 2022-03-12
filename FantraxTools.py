from UpdateTeamSheets.src.sheets_connect import SheetsService
import FantraxUtils.FantraxUtils as FantraxUtils
from FantraxUtils import Team
import datetime

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
    service = SheetsService()
    service.execute_sheets_operation('write', worksheet_id=workbookId, sheet_name=team.name, data=[keys_data])
    for player in team:
        # TODO consider if there is a batch write that maybe counts as less operations
        print('writing player {} from team {}'.format(player, team.name))
        write_player_to_team_sheet(team.name, workbookId, player)

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

        remove_leftover_sheet_from_arb_workbook(currentWorkbookId)
    
    return workbookIds

def main():
    workbookIds = create_arb_workbooks()
    teamsList = FantraxUtils.create_all_teams()
    for team in teamsList:
        for arbTeam in teamsList:
            wbid = workbookIds[team.name]
            print('for team {} and wbid {} and arbTeam {}, starting roster export'.format(team, wbid, arbTeam))
            export_roster_to_arb_workbook(arbTeam, wbid)

if __name__ == '__main__':
    main()