class Player(dict):    
    
    def __init__(self, kvps):
        super(Player, self).__init__(kvps)
        self['Salary'] = int(self['Salary'])
    
    def __repr__(self):
        return self['Player']
        
    def GetStatus(self):
        return self['Status']

    def UpdateSalary(self, updateValue):
        self['Salary'] = self['Salary'] + updateValue

def main():
    myPlayer = Player('Mike Trout')
    print(myPlayer)
    
if __name__ == '__main__':
    main()