from random import randint

class LevelGenerator:
    """
    this class produces a new map . i admit. it's logic is quite twisted but it's neccessary or the levels would be as simple as the logic you used.
    and we dont want the players to suffer death from boredom. doctors dont recommend it.
    """
    def __init__(self):
        self.tilemap ={}
        self.cubeTiles=[0,0,None,None]
        self.movementHistory=["0_0_None_None"]
    
    def generateLevel(self,effektiveMoves = 20):
        self.movementHistory=["0_0_None_None"]
        self.cubeTiles=[0,0,None,None]
        count = 0
        failcount = 0
        directions = ["up","down","left" , "right" ]
        while ( len( self.movementHistory ) < effektiveMoves ):
            print("step1:",self.movementHistory)
            self.fakeMove( directions[randint(0,3)] )
            print("step2:",self.movementHistory)
            indexnumber = self.movementHistory.index(self.movementHistory[-1])
            print("index:", indexnumber)
            while len(self.movementHistory) > indexnumber+1:
                print(self.movementHistory.pop())
            
        while (not "None" in self.movementHistory[-1]):
            self.movementHistory.pop()
        
        print(len(self.movementHistory),self.movementHistory[-1])
        return self.createLevelFromHistory(self.movementHistory)
        
        
    def createLevelFromHistory(self,history):
        tiles = []
        for number in range(0,len(history) ):
            tilestring =  history[number].split("_")
            strpos1 = "Pos="+tilestring[0]+"_"+tilestring[1]  
            if strpos1 not in tiles:
                tiles.append(strpos1)
            if tilestring[2] != "None":
                strpos2 = "Pos="+tilestring[2]+"_"+tilestring[3]  
                if strpos2 not in tiles:
                    tiles.append(strpos2)
        myMapString = "<Type=start,Pos=0_0>"
        for number in range(1,len(tiles)-1 ):
            myMapString +=  "<Type=tile,"+tiles[number]+">"
        myMapString += "<Type=goal,"+tiles[-1]+">"
        return myMapString
        
    def getCubeTiles(self):
        tiles = self.movementHistory[-1].split("_")
        if tiles[2] == "None":
            self.cubeTiles = [int(tiles[0]),int(tiles[1]),None,None]
        else:
            self.cubeTiles = [int(tiles[0]),int(tiles[1]),int(tiles[2]),int(tiles[3])]
        return self.cubeTiles
    
    
    def setCubeTiles(self,x1,y1,x2=None,y2=None):
        newPositionString = str(x1)+"_"+str(y1)+"_"+str(x2)+"_"+str(y2)  # looks like 12_5_None_None 
        self.cubeTiles= [x1,y1,x2,y2]
        self.movementHistory.append(newPositionString)
        print("new move was successful", self.cubeTiles)
    
    
    def fakeMoveTest(self, x1,y1,x2=None,y2=None ):
        for i in ["up","down","left","right"]:
            if self.fakeMoveTestCases(i,x1,y1,x2,y2) == 1:
                return 1    
        return 0
    
        
    def fakeMove(self,direction):
        """
        fakes the rotation of the cube.
        """
        x1,y1,x2,y2 = self.getCubeTiles()
        print("current position", x1,y1,x2,y2) 
        if self.cubeTiles[2] == None :
            #case1 : cube is standing upright
 
            if direction == "right":
                self.setCubeTiles( x1, y1+1 ,x1 , y1+2 )               
            if direction == "left":
                self.setCubeTiles( x1, y1-2 ,x1 , y1-1 )               
            if direction == "up":
                self.setCubeTiles( x1-2, y1 ,x1-1 , y1 )                          
            if direction == "down":
                self.setCubeTiles( x1+1, y1 ,x1+2 , y1 )          
            
        elif x1 == x2:  #if aligned to y-axis (heck i know but precision issues... you know?)
            if direction == "right":
                self.setCubeTiles( x1, y1+2  )
            if direction == "left":
                self.setCubeTiles( x1, y1-1)
            if direction == "up":
                self.setCubeTiles( x1-1, y1, x2-1, y2 )        
            if direction == "down":
                self.setCubeTiles( x1+1, y1, x2+1, y2 )


        elif y1 == y2 : #if it is alligned to x-axis.. (math sux i know but we need tollerance)
            if direction == "right":
                self.setCubeTiles( x1, y1+1, x2, y2+1 )      
            if direction == "left":
                self.setCubeTiles( x1, y1-1, x2, y2-1 )   
            if direction == "up":
                self.setCubeTiles( x1-1, y1  )       
            if direction == "down":
                self.setCubeTiles( x1+2, y1  )

        #this sorta.. doesnt belong here.. but i dunno where to put it yet.
        #x1,y1,x2,y2 = self.getCubeTiles()
        #checkresult = checkMove(self.level.levelNode,self.getCubeTiles(),self.sounds)

