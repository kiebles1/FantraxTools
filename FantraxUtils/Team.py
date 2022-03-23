import operator
from FantraxUtils.Player import Player

class Team(list):

    def __init__(self, name, teamId):
        self.name = name
        self.teamId = teamId

    def __repr__(self):
        return self.name

    def CheckRules(self):
        result = self.ValidateMinorsSize()
        print(self.name + ': ' + str(result))
        
    def UpdatePlayerSalary(self, playerName, updateValue):
        print('update has {}: {}'.format(playerName, updateValue))
        for player in self:
            if 'Guerrero' in player['Player']:
                print('found vlad')
            if player['Player'] == playerName:
                print('updating sal for {}'.format(player))
                player.UpdateSalary(updateValue)

    def UpdateAllMajorsSalaries(self, updateValue):
        for player in self:
            if player['Status'] != 'min':
                player['Salary'] += 2

    def ValidateMinorsSize(self):
        result = True
        count = 0;
        for p in self:
            if p.GetStatus() == 'Min':
                count += 1
        
        if count > 10:
            result = False

        return result
    
    @property
    def workbookId(self):
        return self.workbookId

    @workbookId.setter
    def workbookId(self, workbookId):
        self.workbookId = workbookId