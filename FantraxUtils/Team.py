import operator
from FantraxUtils.Player import Player

class Team(list):

    def __init__(self, name, teamId):
        self.name = name
        self.teamId = teamId
        self.hashDict = dict()

    def __repr__(self):
        return self.name

    def append(self, player):
        self.hashDict[player['ID']] = player
        super(Team, self).append(player)

    def CheckRules(self):
        result = self.ValidateMinorsSize()
        print(self.name + ': ' + str(result))
        
    def UpdatePlayerSalary(self, playerName, updateValue):
        for player in self:
            if player['Player'] == playerName:
                player.UpdateSalary(updateValue)

    def UpdateAllMajorsSalaries(self, updateValue):
        for player in self:
            if player['Status'] != 'Min':
                player.UpdateSalary(updateValue)

    def ValidateMinorsSize(self):
        result = True
        count = 0;
        for p in self:
            if p.GetStatus() == 'Min':
                count += 1
        
        if count > 10:
            result = False

        return result

    def GetPlayerForID(self, id):
        try:
            return self.hashDict[id]
        except KeyError:
            return None
    
    @property
    def workbookId(self):
        return self.workbookId

    @workbookId.setter
    def workbookId(self, wbid):
        self._workbookId = wbid

    @workbookId.getter
    def workbookId(self, wbid):
        self._workbookId = wbid