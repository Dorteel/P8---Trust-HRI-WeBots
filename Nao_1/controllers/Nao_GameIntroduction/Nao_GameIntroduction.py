from controller import Robot, Keyboard, Motion, Display, Supervisor
import time
import os

class Nao (Supervisor):
    PHALANX_MAX = 8
    recorded = False
    doRecording = True
    resetSitting = True
    endMotion = False

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
        self.handWave = Motion('../../motions/Meyer/HandWave.motion')
        self.SitDown = Motion('../../motions/Meyer/SitDown.motion')
        self.Standby = Motion('../../motions/Meyer/Standby.motion')
        self.SitStandby = Motion('../../motions/Meyer/SitStandby.motion')
        self.Roll = Motion('../../motions/Meyer/Rolling.motion')
        self.Cheat = Motion('../../motions/Meyer/Cheat.motion')
        self.LookDown = Motion('../../motions/Meyer/LookDown.motion')
        self.LookUp = Motion('../../motions/Meyer/LookUp.motion')
        
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
        if not self.toRecord[fileName] and self.doRecording and not os.path.isfile(self.path + fileName + '.mp4'):
            self.movieStartRecording(self.path + fileName + '.mp4', 1280, 720, 1337, 100, 1, False)
            #self.movieStartRecording('../../Movies/' + fileName + '.mp4', 1280, 720, 1337, 100, 1, False)
            motion.setLoop(False)
            motion.play()
            while not motion.isOver():
                robot.step(self.timeStep)
            if motion.isOver():
                self.movieStopRecording()
                self.toRecord[fileName] = True
                self.simulationSetMode(0)
                time.sleep(5)
                self.simulationSetMode(1)      
        else:
            print(fileName + ' already recorded.')
            pass

    def __init__(self):
        Supervisor.__init__(self)
        self.currentlyPlaying = False
        
        self.nao = self.getFromDef('NAO')
        self.view = self.getFromDef('VIEW')
        self.viewAngle = self.view.getField('orientation')
        self.viewPosition = self.view.getField('position')
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
                files.append(os.path.isfile(self.path + key + '.mp4'))
            return True if all(files) else False
        return False
        
    def moveCamera(self):
        startOrientation = [-1, 0, 0, 0.87382]
        startPosition = [-2.71, 1, -0.25]
        midPos = [-2.66, 0.9, -1.5]
        endPos=[-2.66, 1.18, -2.85]
        endOr=[0, 1, 1, 3.14]
        self.viewAngle.setSFRotation(startOrientation)
        
        
        # fade away:
        diffX = endPos[1]-midPos[1]
        diffY = endPos[2]-midPos[2]
        Y = midPos[2]
        self.viewAngle.setSFRotation(endOr)
        for x in range(900, 1180):
            Y += diffY/diffX/1000
            self.viewPosition.setSFVec3f([-2.66, x/1000, Y]) 
            if [-2.66, round(x/1000,2), round(Y,2)] == endPos:
                self.endMotion = True
            print(Y)
            robot.step(self.timeStep)
       
    def run(self):
   
        while robot.step(self.timeStep) != -1:
            # Here goes the looOOoop
            self.moveCamera()
            if robot.step(self.timeStep) == -1 or self.endMotion:
                break                

# create the Robot instance and run main loop
robot = Nao()
robot.run()
