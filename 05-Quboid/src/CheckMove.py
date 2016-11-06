
from random import randint

def checkMove(level, pos , sounds = None):
    """
    the game rules for valid movements are implemented here,
    return value of 0 means, everything is fine, 1 means loosing for some ridiculus reason,
    a return value of 2 means, level won.
    as you can imagine. there is a lot more space for new and whicked ways to loose.
    """
    x1,y1,x2,y2 = pos
    
    tile1 = level.find("=Pos="+str(x1)+"_"+str(y1))
    tile2 = None
    if x2 != None :
      tile2 = level.find("=Pos="+str(x2)+"_"+str(y2))
    #print pos
    if sounds != None:
        soundChecks(tile1,tile2,sounds)
    """
    if tile1.getTag("Type") == "weaktile":
        if sounds != None:
            sounds.playSound("kr"+str(randint(0,1))+".wav")
            "print crackling sound"
    """
    
    if tile1.isEmpty() == True:
        print("you lost!")
        return 1   
    
    if x2 != None and tile2.isEmpty() == True :  #means. if there is supposed to be a tile under the cube but there is none..
        print("you lost!..once more")
        return 1
    
    if tile1.getTag("Type") == "weaktile" and tile2 == None :
        print("loosing due to broken weaktile")
        return 1
    
    if tile1.getTag("Type") == "goal" and x2 == None:
        print("you won, switching to next level!")
        return 2
    
    else:
        return 0

def soundChecks(tile1,tile2,sounds):
    #check for crackling sound
    if tile1.isEmpty() == False:
        if tile2 != None:
            if tile2.isEmpty()==False:
              if tile1.getTag("Type") == "weaktile" or  tile2.getTag("Type") == "weaktile" :
                sounds.playSound("kr"+str(randint(0,1)+1)+".wav")
    
