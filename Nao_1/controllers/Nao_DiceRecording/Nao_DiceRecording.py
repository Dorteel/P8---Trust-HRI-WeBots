from controller import Robot, Keyboard, Motion, Display, Supervisor
import time
import os
import random

class Nao (Supervisor):
    PHALANX_MAX = 8
    recorded = False
    doRecording = True
    resetSitting = True

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
        self.SitDown = Motion('../../motions/Meyer/SitDown.motion')

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
        self.diceX = [-2.82, -2.67]
        self.diceZ = [-0.59, -0.46]
        self.diceY = 0.56
        self.dices = {
        '1':[[0.863723, 0, -0.503967, -3.14014],[0.863723, 0, -0.503967, -3.14014],[1, 0, 0, -3.14]],
        '2':[[0.71337, 0.494744, 0.496319, -1.89931], [0.968969, 0.174507, 0.175062, -1.59914],[1, 0, 0, -1.56762]],
        '3':[[0.415933, -0.414613, -0.80938, 1.77762],[0.31451, -0.313513, 0.895987, -1.67725],[0, 0, 1, -1.56762]],
        '4':[[0.6131, 0.613097, 0.498217, 2.21715],[-0.434496, -0.434495, -0.78894, -1.80567],[0, 0, 1, 1.56762]],
        '5':[[0.890263, 0.321538, -0.322561, 1.68362], [-0.872445, -0.345023, 0.346121, -1.70369],[-1, 0, 0, -1.56762]],
        '6':[[-2.15649e-06, -1, 2.75363e-07, 2.06914],[0, 1, 0 , 0], [1.72542e-06, 1, -8.27104e-07, -2.70914]]}
        self.dicePositions = {
        '32':[[],[]],
        '41':[[],[]],
        '42':[[],[]],
        '43':[[],[]],
        '51':[[],[]],
        '52':[[],[]],
        '53':[[],[]],
        '54':[[],[]],
        '61':[[],[]],
        '62':[[],[]],
        '63':[[],[]],
        '64':[[],[]],
        '65':[[],[]],
        '11':[[],[]],
        '22':[[],[]],
        '33':[[],[]],
        '44':[[],[]],
        '55':[[],[]],
        '66':[[],[]],
        '13':[[],[]],
        '12':[[],[]]}
        self.toRecord = {
        'SitDown':False}

        self.bodyColour = {
        'Grey':[0.5, 0.5, 0.5]
        }

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
        self.dice1 = self.getFromDef('dice1')
        self.dice2 = self.getFromDef('dice2')
        self.dice1Translation = self.dice1.getField('translation')
        self.dice1Rotation = self.dice1.getField('rotation')
        
        self.dice2Translation = self.dice2.getField('translation')
        self.dice2Rotation = self.dice2.getField('rotation')
        
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
                files.append(os.path.isfile(self.path + key + '.mp4'))
            return True if all(files) else False
        return False
        
        
    def run(self):
        listofImgs = []
        self.SitDown.setLoop(False)
        self.SitDown.play()
        while robot.step(self.timeStep) != -1:
            for colors, values in self.bodyColour.items():
                self.mainColourField.setSFColor(values)
                if self.SitDown.isOver():
                    for d1 in range(1,7):
                        for d2 in range(1,7):
                            for i in range(2):
                                rot1 = self.dices[str(d1)][random.randint(0,2)]
                                rot2 = self.dices[str(d2)][random.randint(0,2)]
                                dist = 0
                                while not dist >= 0.07:
                                    dice1X = random.uniform(self.diceX[0],self.diceX[1])
                                    dice1Z = random.uniform(self.diceZ[0],self.diceZ[1])
                                
                                    dice2X = random.uniform(self.diceX[0],self.diceX[1])
                                    dice2Z = random.uniform(self.diceZ[0],self.diceZ[1])
                                    d1trans = [dice1X, self.diceY, dice1Z]
                                    d2trans = [dice2X, self.diceY, dice2Z]   
                                    dist = sum([(a - b) ** 2 for a, b in zip(d1trans, d2trans)])**0.5
                                self.dice1Rotation.setSFRotation(rot1)
                                self.dice2Rotation.setSFRotation(rot2)
                                self.dice1Translation.setSFVec3f(d1trans)
                                self.dice2Translation.setSFVec3f(d2trans)
                                robot.step(self.timeStep)
                                robot.step(self.timeStep)
                                robot.step(self.timeStep)
                                robot.step(self.timeStep)
                                self.simulationSetMode(0)
                                name = str(d1) + str(d2) +'_' + str(i)
                                self.exportImage( '../../movies/' + "dice/"+ colors + "/" + name + ".jpg", 100)
                                listofImgs.append(name)
                                self.simulationSetMode(1)
                    #self.exportImage( '../../movies/' + "dice/"+ color + "/" + str(self.currentEpisode) + ".jpg", 100)
            if robot.step(self.timeStep) == -1 or len(listofImgs) == 72:
                break                

# create the Robot instance and run main loop
robot = Nao()
robot.run()
