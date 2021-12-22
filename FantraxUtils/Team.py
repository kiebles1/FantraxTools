import operator

class Team(list):

    def __init__(self, name, teamId):
        self.name = name
        self.teamId = teamId

    def __repr__(self):
        return self.name
        
    def CheckRules(self):
        result = self.ValidateMinorsSize()
        print(self.name + ': ' + str(result))
        
    def ValidateMinorsSize(self):
        result = True
        count = 0;
        for p in self:
            if p.GetStatus() == 'Min':
                count += 1
        
        if count > 10:
            result = False
            
        return result
            