from controller import Robot, Keyboard, Motion, Display, Supervisor
import time
import os
import datetime

class Nao (Supervisor):
    PHALANX_MAX = 8
    recorded = False
    doRecording = True
    resetSitting = True
    resetted = True
    recordingStart = datetime.datetime(2020, 5, 2, 16, 43, 27, 97948)
    ready2record = False

    def createDirectory(self):
        if not os.path.isdir(self.path):
            try:
                os.makedirs(self.path)
            except OSError:
                print ("Creation of the directory %s failed" % self.path)
            else:
                print ("Successfully created the directory %s " % self.path)

    # load motion files
    def loadMotionFiles(self):
        self.Standby = Motion('../../motions/Meyer/Standby.motion')
      
    def findDevices(self):
        self.leds = []
        self.leds.append(self.getLED('ChestBoard/Led'))
        self.leds.append(self.getLED('RFoot/Led'))
        self.leds.append(self.getLED('LFoot/Led'))
        self.leds.append(self.getLED('Face/Led/Right'))
        self.leds.append(self.getLED('Face/Led/Left'))
        self.leds.append(self.getLED('Ears/Led/Right'))
        self.leds.append(self.getLED('Ears/Led/Left'))
        
        self.mainColourField = self.nao.getField('mainColor')
        self.secondaryColourField = self.nao.getField('color')
    
    def recordMotion(self, motion, fileName):
        if self.ready2record:
            if self.doRecording:
                self.movieStartRecording(self.path + fileName + '.mp4', 1280, 720, 1337, 100, 1, False)
                #self.movieStartRecording('../../Movies/' + fileName + '.mp4', 1280, 720, 1337, 100, 1, False)
                motion.setLoop(False)
                motion.play()
                while not motion.isOver():
                    robot.step(self.timeStep)
                if motion.isOver():
                    self.movieStopRecording()
                    self.simulationSetMode(0)
                    time.sleep(5)
                    self.simulationSetMode(1)      
            else:
                print(fileName + ' already recorded.')
                pass

    def __init__(self):
        Supervisor.__init__(self)
        self.currentlyPlaying = False
        
        self.toRecord = {'StandBy':False}
        self.bodyColours = {
        'Pink':[1, 0.33, 0.498],
        'Blue':[0, 0.592157, 0.886275],
        'DarkBlue':[0, 0, 0.498039],
        'Green':[0, 0.866667, 0],
        'DarkGreen':[0, 0.572549, 0],
        'Yellow':[1, 1, 0],
        'DarkYellow':[0.5, 0.5, 0],
        'Red':[1, 0, 0],
        'DarkRed':[0.369, 0.047, 0.047],
        'White':[1, 1, 1],
        'Black':[0, 0, 0],
        'Grey':[0.5, 0.5, 0.5]}
        self.eyeColours = {
        'Blue':0x0000FF,
        'Green':0x00FF00,
        'Yellow':0xF7FF00,
        'White':0xFFFFFF,
        'Black':0x000000,
        'Red':0xFF0000}
        self.nao = self.getFromDef('NAO')
        self.findDevices()
        self.timeStep = int(self.getBasicTimeStep())
        # initialize stuff
        self.loadMotionFiles()
        self.translationField = self.nao.getField('translation')
        self.rotationField = self.nao.getField('rotation')

    def setAllLedsColor(self, rgb):
        # these leds take RGB values
        for i in range(0, len(self.leds)):
            self.leds[i].set(rgb)

        # ear leds are single color (blue)
        # and take values between 0 - 255
        self.leds[5].set(rgb & 0xFF)
        self.leds[6].set(rgb & 0xFF)

    def doneAlready(self, main, secondary, eye):
        folderName = main + secondary + eye
        self.path = '../../movies/testing/' + folderName + '/'
        if os.path.isdir(self.path):
            files = []
            for key in self.toRecord:
                fullPath = self.path + key + '.mp4'
                if os.path.isfile(fullPath):
                    t1 = datetime.datetime.fromtimestamp(os.stat(fullPath).st_mtime)
                    return t1 > self.recordingStart
                return False
        return False
        
        
    def run(self):
   
        while robot.step(self.timeStep) != -1:
            # Here goes the looOOoop
            if self.movieIsReady():
                #self.simulationSetMode(0)
                for mainColor, mainValue in self.bodyColours.items():
                    for secColor, secValue in self.bodyColours.items():    
                        for eyeColor, eyeValue in self.eyeColours.items():
                            if not self.doneAlready(mainColor, secColor, eyeColor):
                                print('Recording with \n\tMaincolour:\t{}\n\tSecColor:\t{}\n\tEyecolour:\t{}'.format(mainColor, secColor, eyeColor))
                                self.simulationSetMode(0)
                                self.setAllLedsColor(eyeValue)
                                self.secondaryColourField.setSFColor(secValue)
                                self.mainColourField.setSFColor(mainValue)
                                self.ready2record = True
                                #self.createDirectory()
                                self.simulationSetMode(1)
                                self.recordMotion(self.Standby, 'StandBy')
                                if self.resetted:
                                    self.resetted = False
                                    self.recordMotion(self.Standby, 'StandBy')
                                self.ready2record = False
                                
                                #self.recordMotion(self.Standby, 'StandBy')
                                #self.simulationReset()
                                self.worldReload()
                            else:
                                #print('Recording with {}{}{} has already been done.'.format(mainColor, secColor, eyeColor))
                                pass
                        #self.worldReload()
            if robot.step(self.timeStep) == -1:
                break                

# create the Robot instance and run main loop
robot = Nao()
robot.run()
