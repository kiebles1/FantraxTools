from UpdateTeamSheets.src.sheets_connect import SheetsService
import FantraxUtils.FantraxUtils as FantraxUtils
import datetime

def create_arb_workbook(teamName):
    service = SheetsService()
    workbookId = service.create_worksheet(teamName + '_' + str(datetime.date.today().year))
    return workbookId

def populate_team_sheet(teamName, teamId, workbookId):
    print('not ready')

def write_player_to_team_sheet(teamName, teamId, workbookId, player):
    service = SheetsService()
    service.write_sheet(workbookId, teamName, player)

def add_team_to_arb_workbook(teamName, teamId, workbookId):
    service = SheetsService()
    service.add_sheet(workbookId, teamName)

def remove_leftover_sheet_from_arb_workbook(workbookId):
    service = SheetsService()
    service.delete_sheet(workbookId, 0)

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