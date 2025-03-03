from FantraxUtils.Player import Player

class Team(list):

    # TODO-SK I think these are going to be used for sorting
    HITTER_PROJECTION_CATS = Player.HITTER_PROJECTION_CATS
    PITCHER_PROJECTION_CATS = Player.PITCHER_PROJECTION_CATS

    def __init__(self, name, teamId):
        self.name = name
        self.teamId = teamId
        self.hashDict = dict()

    def __repr__(self):
        return self.name
    
    def _initializeHittingProjections(self):
        self.hrProjection = 0.0
        self.avgProjection = 0.0
        self.obpProjection = 0.0
        self.rProjection = 0.0
        self.rbiProjection = 0.0
        self.sbProjection = 0.0
        self.abProjection = 0.0
        self.paProjection = 0.0
        
        self.avgProjectionNumerator = 0.0
        self.obpProjectionNumerator = 0.0

    def _initializePitchingProjections(self):
        self.wProjection = 0.0
        self.ipProjection = 0.0
        self.svProjection = 0.0
        self.hldProjection = 0.0
        self.kProjection = 0.0
        self.eraProjection = 0.0
        self.whipProjection = 0.0
        self.qsProjection = 0.0

        self.eraProjectionNumerator = 0.0
        self.whipProjectionNumerator = 0.0

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
    
    def GeneratePitchingProjections(self):
        self._initializePitchingProjections()
        for player in self:
            if ('SP' in player['Pos'] or 'RP' in player['Pos'] or player['Pos'] == 'P') and player.GetStatus() != 'Min':
                self.wProjection += player['W']
                self.ipProjection += player['IP']
                self.svProjection += player['SV']
                self.hldProjection += player['HLD']
                self.kProjection += player['SO']
                self.qsProjection += player['QS']
                self.eraProjectionNumerator += (player['ERA'] * player['IP'])
                self.whipProjectionNumerator += (player['WHIP'] * player['IP'])
                
    def GenerateHittingProjections(self):
        self._initializeHittingProjections()
        for player in self:
            if 'SP' not in player['Pos'] and 'RP' not in player['Pos'] and player['Pos'] != 'P' and player.GetStatus() != 'Min':
                self.hrProjection += player['HR']
                self.rProjection += player['R']
                self.rbiProjection += player['RBI']
                self.sbProjection += player['SB']
                self.paProjection += player['PA']
                self.abProjection += player['AB']
                self.obpProjectionNumerator += (player['OBP'] * player['PA'])
                self.avgProjectionNumerator += (player['AVG'] * player['AB'])

    def ReportHittingProjections(self):
        print('\tHR: {HR:<4} R: {R:<4} RBI: {RBI:<4} SB: {SB:<4} OBP: {OBP:<4.3f} AVG: {AVG:<4.3f} PA: {PA:<4}'.format(HR=int(self.hrProjection), R=int(self.rProjection), \
                                                                                      RBI=int(self.rbiProjection), SB=int(self.sbProjection), \
                                                                                      OBP=(self.obpProjectionNumerator / self.paProjection),\
                                                                                      AVG=(self.avgProjectionNumerator / self.abProjection),\
                                                                                      PA=int(self.paProjection)
        ))
        
    def ReportPitchingProjections(self):
        print('\tW: {W:<4} IP: {IP:<4} SVHD: {SVHD:<4} K: {K:<4} QS: {QS:<4} ERA: {ERA:<4.3} WHIP: {WHIP:<4.3}'.format(
            W=int(self.wProjection), IP=int(self.ipProjection), SVHD=int(self.svProjection + self.hldProjection), K=int(self.kProjection), \
            QS=int(self.qsProjection), ERA=(self.eraProjectionNumerator / self.ipProjection), WHIP=(self.whipProjectionNumerator / self.ipProjection)
        ))

    def GenerateProjections(self):
        print('Team {}'.format(self.name))
        self.GenerateHittingProjections()
        self.GeneratePitchingProjections()

    def ReportProjections(self):
        self.ReportHittingProjections()
        self.ReportPitchingProjections()
    
    @property
    def workbookId(self):
        return self.workbookId

    @workbookId.setter
    def workbookId(self, wbid):
        self._workbookId = wbid

    @workbookId.getter
    def workbookId(self, wbid):
        self._workbookId = wbid