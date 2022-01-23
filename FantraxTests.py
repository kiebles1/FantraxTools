import unittest
import FantraxUtils.FantraxUtils as ftu
import FantraxTools as ftools
import UpdateTeamSheets.src.sheets_connect as sc
import os, os.path

class TestFantraxUtils(unittest.TestCase):
    def testDownloadAll(self):
        ftu.download_all_roster_files(teamsFile='FantraxUtils/cfg/Teams.csv')
        dir = './Rosters'
        self.assertTrue(os.path.isdir(dir))
        self.assertTrue(
            len([name for name in os.listdir(dir) if os.path.isfile(os.path.join(dir, name))]) == 12
        )

    def testPlayerMethods(self):
        plr = ftu.Player({'name': 'Mike Trout', 'Pos': 'OF'})
        self.assertTrue(list(plr.values()) == ['Mike Trout', 'OF'])
        
class TestFantraxTools(unittest.TestCase):
    def testCreateArbSheets(self):
        ftools.create_arb_workbooks()

    def testWritePlayer(self):
        wsid = ftools.create_arb_workbook('testTeam')
        plr = ftu.Player({'Name':'Mike Trout', 'Pos':'OF', 'Salary':'5'})
        ftools.write_player_to_team_sheet('Sheet1', wsid, plr)

class TestSheetsService(unittest.TestCase):
    def create_test_sheet(self):
        self.service = sc.SheetsService()
        self.wsid = self.service.execute_sheets_operation('create', workbook_name='TestSheet')

    def testWriteDictToSheet(self):
        guy = {'name':'Mike Trout','cost':'21', 'pos':'OF'}
        guy = [list(guy.keys()), list(guy.values())]
        self.create_test_sheet()
        self.service.execute_sheets_operation('add_sheet', worksheet_id=self.wsid, sheet_name='test1')
        self.service.execute_sheets_operation('write', worksheet_id=self.wsid, sheet_name='test1', data=guy)

    def testGetSheetIds(self):
        self.create_test_sheet()
        self.service.execute_sheets_operation('get_ids', worksheet_id=self.wsid)

    def testDeleteSheet(self):
        self.create_test_sheet()
        self.service.execute_sheets_operation('add_sheet', worksheet_id=self.wsid, sheet_name='test')
        self.service.execute_sheets_operation('delete_sheet', worksheet_id=self.wsid, sheet_id=0)

if __name__ == '__main__':
    unittest.main()