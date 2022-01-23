from UpdateTeamSheets.src.sheets_connect import SheetsService
import FantraxUtils.FantraxUtils as FantraxUtils
import datetime

def create_arb_workbook(teamName):
    service = SheetsService()
    workbookId = service.execute_sheets_operation('create', workbook_name=teamName + '_' + str(datetime.date.today().year))
    return workbookId

def populate_team_sheet(teamName, teamId, workbookId):
    print('not ready')

def write_player_to_team_sheet(teamName, workbookId, player):
    service = SheetsService()
    # data has to be a 2d list, even if you only have 1 row of data
    service.execute_sheets_operation('write', worksheet_id=workbookId, sheet_name=teamName, data=[list(player.values())])

def add_team_to_arb_workbook(teamName, teamId, workbookId):
    service = SheetsService()
    service.execute_sheets_operation('add_sheet', worksheet_id=workbookId, sheet_name=teamName)

def remove_leftover_sheet_from_arb_workbook(workbookId):
    service = SheetsService()
    service.execute_sheets_operation('delete_sheet', worksheet_id=workbookId, sheet_id=0)

def create_arb_workbooks():
    pairsList = FantraxUtils.get_team_name_id_pairs('./FantraxUtils/cfg/Teams.csv')
    for outerPair in pairsList:
        outerName = outerPair[0]
        outerId = outerPair[1]
        if outerName == 'Team Name':
            continue

        currentWorkbookId = create_arb_workbook(outerName)

        for innerPair in pairsList:
            innerName = innerPair[0]
            innerId = innerPair[1]
            # teams don't need to do their own arb
            if (innerName == 'Team Name') or (innerName == outerName):
                continue

            add_team_to_arb_workbook(innerName, innerId, currentWorkbookId)

        remove_leftover_sheet_from_arb_workbook(currentWorkbookId)

        

if __name__ == '__main__':
    FantraxUtils.download_teams_to_sheets()