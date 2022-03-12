import unittest
import FantraxUtils.FantraxUtils as ftu
import FantraxTools as ftools
import UpdateTeamSheets.src.sheets_connect as sc
import os, os.path
import sys

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
        
        svc = sc.SheetsService()
        data = svc.execute_sheets_operation('read', worksheet_id=wsid, sheet_name='Sheet1')
        self.assertTrue(list(data) == [list(plr.values())])

    def testWriteHeaders(self):
        wsid = ftools.create_arb_workbook('testTeam')
        plr = ftu.Player({'Name':'Mike Trout', 'Pos':'OF', 'Salary':'5'})
        ftools.write_headers_to_team_sheet(wsid, 'Sheet1', list(plr.keys()))
        ftools.write_player_to_team_sheet('Sheet1', wsid, plr)

    def testRosterToWorkbook(self):
        wsid = ftools.create_arb_workbook('testTeam')
        team = ftu.Team('Sheet1', 'abcdefg')
        team.append(ftu.Player({'Name':'Mike Trout', 'Pos':'OF', 'Salary':'5'}))
        team.append(ftu.Player({'Name':'Mookie Betts', 'Pos':'OF', 'Salary':'27'}))
        team.append(ftu.Player({'Name':'Raphael Devers', 'Pos':'3B', 'Salary':'22'}))
        ftools.write_headers_to_team_sheet(wsid, 'Sheet1', list(team[0].keys()))
        ftools.export_roster_to_arb_workbook(team, wsid)

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
        ids = self.service.execute_sheets_operation('get_ids', worksheet_id=self.wsid)

    def testDeleteSheet(self):
        self.create_test_sheet()
        self.service.execute_sheets_operation('add_sheet', worksheet_id=self.wsid, sheet_name='test')
        self.service.execute_sheets_operation('delete_sheet', worksheet_id=self.wsid, sheet_id=0)

    def testProtectRange(self):
        self.create_test_sheet()
        guy = {'name':'Mike Trout','cost':'21', 'pos':'OF'}
        guy = [list(guy.keys()), list(guy.values())]
        self.service.execute_sheets_operation('write', worksheet_id=self.wsid, sheet_name='Sheet1', data=guy)

        self.service.execute_sheets_operation('protect_range', worksheet_id=self.wsid, sheet_name='test', data_range=None)

    def testSheetIdFromName(self):
        self.create_test_sheet()
        self.service.execute_sheets_operation('add_sheet', worksheet_id=self.wsid, sheet_name='test')
        sheet_id = self.service.execute_sheets_operation('get_id_from_name', worksheet_id=self.wsid, sheet_name='test')
        sys.stdout = sys.__stdout__
        print('id: {}'.format(sheet_id))

    def testDataValidation(self):
        self.create_test_sheet()
        guy = {'name':'Mike Trout','cost':'21', 'pos':'OF'}
        guy = [list(guy.keys()), list(guy.values())]
        self.service.execute_sheets_operation('add_sheet', worksheet_id=self.wsid, sheet_name='test')
        self.service.execute_sheets_operation('write', worksheet_id=self.wsid, sheet_name='test', data=guy)

        ret = self.service.execute_sheets_operation('apply_data_validation', worksheet_id=self.wsid, sheet_name='test')
        sys.stdout = sys.__stdout__
        print(ret)

if __name__ == '__main__':
    unittest.main()