

class Sounds(object):
    def __init__(self):
        self.soundlist = [
            ["stonerotate.wav",1],
            ["finish.wav",1],
            ["kr1.wav",.3],
            ["kr2.wav",.3],
            ["drop4.wav",1],
            ["drop3.wav",1],
            ["drop2.wav",1],
            ["drop1.wav",1],
            ["nyon.wav",1],
             ]
        self.soundDict={}
        
        for sound in self.soundlist:
            self.soundDict[sound[0]] = loader.loadSfx("./sounds/"+sound[0])
            self.soundDict[sound[0]].setVolume(sound[1])
    
    def playSound(self,soundname):
        if soundname in self.soundDict:
            self.soundDict[soundname].play()
        else:
            print("sound not found",soundname)
