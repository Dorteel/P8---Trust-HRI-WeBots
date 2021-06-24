# Copyright 1996-2020 Cyberbotics Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Example of Python controller for Nao robot.
   This demonstrates how to access sensors and actuators"""

from controller import Robot, Keyboard, Motion, Display, Supervisor

#master = Supervisor()

class Nao (Supervisor):
    PHALANX_MAX = 8

    # load motion files
    def loadMotionFiles(self):
        self.handWave = Motion('../../motions/HandWave.motion')
        self.testingMotion = Motion('../../motions/sittingMotion.motion')
        self.forwards = Motion('../../motions/Forwards50.motion')
        self.backwards = Motion('../../motions/Backwards.motion')
        self.sideStepLeft = Motion('../../motions/SideStepLeft.motion')
        self.sideStepRight = Motion('../../motions/SideStepRight.motion')
        self.turnLeft60 = Motion('../../motions/TurnLeft60.motion')
        self.turnRight60 = Motion('../../motions/TurnRight60.motion')

    def startMotion(self, motion):
        # interrupt current motion
        if self.currentlyPlaying:
            self.currentlyPlaying.stop()

        # start new motion
        motion.play()
        self.currentlyPlaying = motion


    def setAllLedsColor(self, rgb):
        # these leds take RGB values
        for i in range(0, len(self.leds)):
            self.leds[i].set(rgb)

        # ear leds are single color (blue)
        # and take values between 0 - 255
        self.leds[5].set(rgb & 0xFF)
        self.leds[6].set(rgb & 0xFF)


    def findAndEnableDevices(self):
        # get the time step of the current world.
        self.timeStep = int(self.getBasicTimeStep())

        # there are 7 controlable LED groups in Webots
        self.leds = []
        self.leds.append(self.getLED('ChestBoard/Led'))
        self.leds.append(self.getLED('RFoot/Led'))
        self.leds.append(self.getLED('LFoot/Led'))
        self.leds.append(self.getLED('Face/Led/Right'))
        self.leds.append(self.getLED('Face/Led/Left'))
        self.leds.append(self.getLED('Ears/Led/Right'))
        self.leds.append(self.getLED('Ears/Led/Left'))

        # get phalanx motor tags
        # the real Nao has only 2 motors for RHand/LHand
        # but in Webots we must implement RHand/LHand with 2x8 motors
        self.lphalanx = []
        self.rphalanx = []
        self.maxPhalanxMotorPosition = []
        self.minPhalanxMotorPosition = []
        for i in range(0, self.PHALANX_MAX):
            self.lphalanx.append(self.getMotor("LPhalanx%d" % (i + 1)))
            self.rphalanx.append(self.getMotor("RPhalanx%d" % (i + 1)))

            # assume right and left hands have the same motor position bounds
            self.maxPhalanxMotorPosition.append(self.rphalanx[i].getMaxPosition())
            self.minPhalanxMotorPosition.append(self.rphalanx[i].getMinPosition())

        # shoulder pitch motors
        self.RShoulderPitch = self.getMotor("RShoulderPitch")
        self.LShoulderPitch = self.getMotor("LShoulderPitch")

        # keyboard
        self.keyboard = self.getKeyboard()
        self.keyboard.enable(10 * self.timeStep)

    def __init__(self):
        Supervisor.__init__(self)
        self.currentlyPlaying = False

        # initialize stuff
        self.findAndEnableDevices()
        self.loadMotionFiles()

    def run(self):
        #self.movieStartRecording('../../Movies/testRecording.mp4', 1280, 720, 1337, 100, 1, False)
        self.testingMotion.setLoop(True)
        self.testingMotion.play()
        
        while robot.step(self.timeStep) != -1:
            if self.testingMotion.isOver:
                print('Motion is over')

        self.testingMotion.setLoop(False)
        
        while True:
            key = self.keyboard.getKey()
            
            if self.testingMotion.isOver:
                self.movieStopRecording()
            elif key == Keyboard.RIGHT:
                self.startMotion(self.sideStepRight)
            elif key == Keyboard.UP:
                self.startMotion(self.forwards)
            elif key == Keyboard.DOWN:
                self.startMotion(self.backwards)
            elif key == Keyboard.LEFT | Keyboard.SHIFT:
                self.startMotion(self.turnLeft60)
            elif key == Keyboard.RIGHT | Keyboard.SHIFT:
                self.startMotion(self.turnRight60)
            elif key == ord('7'):
                self.setAllLedsColor(0xff0000)  # red
            elif key == ord('8'):
                self.setAllLedsColor(0x00ff00)  # green
            elif key == ord('9'):
                self.setAllLedsColor(0x0000ff)  # blue
            elif key == ord('0'):
                self.setAllLedsColor(0x3a1e08)  # off

            if robot.step(self.timeStep) == -1:
                break


# create the Robot instance and run main loop
robot = Nao()
robot.run()
