import operator
from FantraxUtils.Player import Player

class Team(list):

    def __init__(self, name, teamId):
        self.name = name
        self.teamId = teamId
        self.hashDict = dict()

    def __repr__(self):
        return self.name
    
    def _initializeProjections(self):
        self._hrProjection = 0.0
        self._avgProjection = 0.0
        self._obpProjection = 0.0
        self._rProjection = 0.0
        self._rbiProjection = 0.0
        self._sbProjection = 0.0
        self._abProjection = 0.0
        self._paProjection = 0.0
        
        self._avgProjectionNumerator = 0.0
        self._obpProjectionNumerator = 0.0

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
        
    def ReportProjections(self):
        self._initializeProjections()
        for player in self:
            if player.GetStatus() != 'Min':
                self._hrProjection += player['HR']
                self._rProjection += player['R']
                self._rbiProjection += player['RBI']
                self._sbProjection += player['SB']
                self._paProjection += player['PA']
                self._abProjection += player['AB']
                self._obpProjectionNumerator += (player['OBP'] * player['PA'])
                self._avgProjectionNumerator += (player['AVG'] * player['AB'])

        print('Team {}'.format(self.name))
        print('\tHR: {HR}\n\tR: {R}\n\tRBI: {RBI}\n\tSB: {SB}\n\tOBP: {OBP}\n\tAVG: {AVG}\n\tPA: {PA}'.format(HR=self._hrProjection, R=self._rProjection, \
                                                                                      RBI=self._rbiProjection, SB=self._sbProjection, \
                                                                                      OBP=(self._obpProjectionNumerator / self._paProjection),\
                                                                                      AVG=(self._avgProjectionNumerator / self._abProjection),\
                                                                                      PA=self._paProjection))
    
    @property
    def workbookId(self):
        return self.workbookId

    @workbookId.setter
    def workbookId(self, wbid):
        self._workbookId = wbid

    @workbookId.getter
    def workbookId(self, wbid):
        self._workbookId = wbid