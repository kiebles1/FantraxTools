from icecream import ic
from Sheets.src.sheets_connect import SheetsService, TRANSLATOR_SPREADHSHEET_ID

class Player(dict):
    _translationTable = None
    
    def __init__(self, kvps):
        super(Player, self).__init__(kvps)
        self['Salary'] = int(self['Salary'])
        self._translationTable = None
    
    def __repr__(self):
        return self['Player']        
        
    def _FindFGID(self):
        if Player._translationTable is None:
            service = SheetsService()
            Player._translationTable = service.execute_sheets_operation('read', worksheet_id=TRANSLATOR_SPREADHSHEET_ID, sheet_name='Sheet1')

        for row in Player._translationTable:
            if (len(row) > 37) and (row[37] == self['ID']):
                ic('Player {} has Fantrax ID {} and Fangraphs ID {}'.format(self['Player'], row[37], row[8]))
                self['FangraphsID'] = row[8]
                break
            else:
                self['FangraphsID'] = -1

    def GetFGID(self):
        if 'FangraphsID' not in self.keys():
            self._FindFGID()
        
        return self['FangraphsID']

    def GetStatus(self):
        return self['Status']

    def UpdateSalary(self, updateValue):
        self['Salary'] = self['Salary'] + updateValue

def main():
    myPlayer = Player('Mike Trout')
    print(myPlayer)
    
if __name__ == '__main__':
    main()