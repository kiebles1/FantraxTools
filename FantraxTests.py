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
        
class TestFantraxTools(unittest.TestCase):
    def testCreateArbSheets(self):
        ftools.create_arb_workbooks()

class TestSheetsService(unittest.TestCase):
    def create_test_sheet(self):
        self.service = sc.SheetsService()
        self.wsid = self.service.create_worksheet('TestSheet')

    def testWriteDictToSheet(self):
        guy = {'name':'Mike Trout','cost':'21', 'pos':'OF'}
        guy = [list(guy.keys()), list(guy.values())]
        self.create_test_sheet()
        self.service.add_sheet(self.wsid, 'test1')
        self.service.write_sheet(self.wsid, 'test1', guy)

    def testGetSheetIds(self):
        self.create_test_sheet()
        self.service.get_sheet_ids(self.wsid)

    def testDeleteSheet(self):
        self.create_test_sheet()
        self.service.add_sheet(self.wsid, 'test')
        self.service.delete_sheet(self.wsid, 0)

if __name__ == '__main__':
    unittest.main()