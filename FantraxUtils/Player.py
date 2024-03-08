from icecream import ic
import csv
from Sheets.src.sheets_connect import SheetsService, TRANSLATOR_SPREADHSHEET_ID

class Player(dict):
    _HITTER_PROEJCTION_CATS = ['AB', 'PA', 'AVG', 'HR', 'R', 'RBI', 'OBP', 'SB']
    _PITCHER_PROEJCTION_CATS = ['W', 'IP', 'SV', 'HLD', 'SO', 'ERA', 'WHIP', 'QS']

    _translationTable = None
    _hitterProjections = None
    _picherProjections = None
    
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

    def _readHitterFile(self, hitterFile):
        if Player._hitterProjections is None:
            Player._hitterProjections = []

        keys = []
        with open(hitterFile, newline='') as csvfile:
            projReader = csv.reader(csvfile, delimiter=',')
            for row in projReader:
                if row[0] == 'Team':
                    keys = row
                else:
                    Player._hitterProjections.append(dict(zip(keys, row)))

    def _projectHitter(self):
        playerFound = False
        for proj in Player._hitterProjections:
            if proj['playerid'] == self['FangraphsID']:
                ic('Projections for {} are {}'.format(self, proj))
                playerFound = True
                for stat in Player._HITTER_PROEJCTION_CATS:
                    self[stat] = float(proj[stat])
                
                break

        # if a player doesn't have fangraphs projections, assume we don't want to know about them
        if not playerFound:
            self['Status'] = 'Min'

    def GetFGID(self):
        if 'FangraphsID' not in self.keys():
            self._FindFGID()
        
        return self['FangraphsID']

    def GetStatus(self):
        return self['Status']

    def UpdateSalary(self, updateValue):
        self['Salary'] = self['Salary'] + updateValue

    def Project(self, hitterFile=None, pitcherFile=None):
        if Player._hitterProjections is None:
            self._readHitterFile(hitterFile)
            print('reading new hitter projection file {}'.format(hitterFile))
        
        if pitcherFile is not None:
            # self._read
            print('reading new pitcher projection file {}'.format(pitcherFile))

        if 'SP' in self['Pos'] or 'RP' in self['Pos']:
            print('skipping pitchers for now')
        else:
            self._projectHitter()

def main():
    myPlayer = Player('Mike Trout')
    print(myPlayer)
    
if __name__ == '__main__':
    main()