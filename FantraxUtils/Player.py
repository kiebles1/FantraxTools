class Player(dict):    
    
    def __init__(self, kvps):
        super(Player, self).__init__(kvps)
    
    def __repr__(self):
        return self['Player']
        
    def GetStatus(self):
        return self['Status']

def main():
    myPlayer = Player('Mike Trout')
    print(myPlayer)
    
if __name__ == '__main__':
    main()