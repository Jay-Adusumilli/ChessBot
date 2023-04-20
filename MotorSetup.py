import RPi.GPIO as GPIO
from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
import inspect
import math
from time       import sleep
import board
from adafruit_servokit import ServoKit
import adafruit_pca9685
from Pi_Setup import Communication
import json


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


# factory = PiGPIOFactory()
# 
# servo1 = Servo(12, min_pulse_width=0.125/1000, max_pulse_width=.725/1000, pin_factory=factory)
# servo2 = Servo(13, min_pulse_width=0.13/1000, max_pulse_width=0.6/1000, pin_factory=factory)
def read_from_json_file(file_name):
    with open(file_name, 'r') as f:
        data = json.load(f)
        return data


class RobotMath():
    def __init__(self):
        pass
    
    def baseAngle(self, currentCoord, desiredCoord):
        rad = math.atan((desiredCoord[1]-currentCoord[1])/(desiredCoord[0]-currentCoord[0]))
        return math.degrees(rad)
    
    def frame0position(self, ang, mag):
        rad = math.radians(ang)
        y = math.cos(rad)*mag
        z = math.sin(rad)*mag
        return y,z
    
    def frame1position(self, ang, mag):
#         print(ang,mag)
        rad = math.radians(ang)
        y = math.cos(rad)*mag
        z = math.sin(rad)*mag
        return y,z
        
    def frame2position(self, ang, mag):
#         print(ang,mag)
        rad = math.radians(ang)
        y = math.cos(rad)*mag
        z = math.sin(rad)*mag
        return y,z
    
    def frame3position(self, ang, mag):
        y = math.sin(ang)*mag
        z = math.cos(ang)*mag
        return y,z
    

class Servo():
    def __init__(self):
        self.controller = Communication()
        
    def Set(self, i , currentAngle):
        self.controller.PCA(i, currentAngle)
    
    def CCW(self,i , currentAngle):
        if i == 5:
            currentAngle += 1
            self.controller.PCA(i, currentAngle)
            return currentAngle
        else:
            currentAngle += .25
            self.controller.PCA(i, currentAngle)
            return currentAngle
        
    def CW(self, i, currentAngle):
        if i == 5:
            currentAngle -= 1
            self.controller.PCA(i, currentAngle)
            return currentAngle
        else:
            currentAngle -= .25
            self.controller.PCA(i, currentAngle)
            return currentAngle
        
class Arm():
    def __init__(self, length, direction):
        self.length = length
        self.direction = direction
        self.servo = Servo()
        self.set = 0
        
    def setAngle(self, i, currentAngle):
        while self.set <= 4:
            self.servo.Set(i, currentAngle)
            self.set += 1
        
        
    def plusAngle(self, i, currentAngle):
        return self.servo.CCW(i, currentAngle)
    
    def minusAngle(self, i, currentAngle):
        return self.servo.CW(i,currentAngle)
        
class Base():
    def __init__(self):
        self.dimensions = [5, 2, 2]
        

class startAngle():
    def __init__(self, starting):
        self.startingAngle = startingAngle
        
    
class RobotController():
    def __init__(self, currentAngle, Armlength):
        
        self.Armlength = Armlength
        self.currentAngle = currentAngle
        self.base = Base()
        self.servoDirection = [1,1,1,1]
        self.Arms = [Arm(Armlength[0], self.servoDirection, ), Arm(Armlength[1], self.servoDirection), Arm(Armlength[2], self.servoDirection), Arm(Armlength[3], self.servoDirection), Arm(Armlength[3], self.servoDirection)] 
         
    def numberServos(self, desiredAngle):
        servoNum = list(range(5))
        for i in range(len(servoNum)):
            if self.currentAngle[i] != desiredAngle[i]:
                servoNum[i] = 1
            else:
                servoNum[i] = 0
        return servoNum
    
    def servoCheck(self, desiredAngle):
        count = 0
        for i in range(len(self.numberServos(desiredAngle))):
            if self.numberServos(desiredAngle)[i] == 1:
                count += 1
        return count
        
    def servoMove(self, desiredAngle):
        count = self.servoCheck(desiredAngle)
        while count > 0:
#             print(count)
            self.smoothMove(desiredAngle)
            count = self.servoCheck(desiredAngle)
            
    def setStart(self, ang):
        for i in range(len(ang)):
            self.Arms[i].setAngle(i ,ang[i])
         
    def smoothMove(self, desiredAngle):
        servoNum = self.numberServos(desiredAngle)
#         print(self.currentAngle)
        for i in range(len(servoNum)):
            if servoNum[i] == 1:
                if self.currentAngle[i] < desiredAngle[i]:
                    self.currentAngle[i] = self.Arms[i].plusAngle(i, self.currentAngle[i])
#                     print(self.currentAngle[i])
                elif self.currentAngle[i] > desiredAngle[i]:
                    self.currentAngle[i] = self.Arms[i].minusAngle(i, self.currentAngle[i])
#                     print(self.currentAngle[i])
                else:
                    self.currentAngle[i] = self.Arms[i].setAngle(i , self.currentAngle[i])
            sleep(.0005)
            

    
class chessBoard():
    def __init__(self):
        self.boardRow = [8, 7, 6, 5, 4, 3, 2, 1]
        self.boardCol = ['a','b','c','d','e','f','g','h']
        self.boardLabels = []
        for i, row in enumerate(self.boardRow):
            temp_array = []
            for j, col in enumerate(self.boardCol):
                temp_array.append(col + str(row))
            self.boardLabels.append(temp_array)
            
#         self.pawn_heights = [[[27,95,50,176,55], [27,84,38,156,40], [37,79,41,130,32], [46,74,41,95,0], [63,75,40,95,0], [88,74,41,95,0], [109,80,46,107,9], [125,91,62,109,10]],
#                             [[37,100,76,132,24], [42,93,61,129,19], [48,89,58,114,10], [58,88,58,99,0], [73,88,58,94,0], [91,93,67,94,0], [105,93,62,109,10], [118,99,77,109,10]],
#                             [[47,106,85,141,35], [52,104,85,124,30], [57,99,75,114,15], [67,97,70,114,15], [80,95,65,124,21], [93,96,65,129,27], [103,96,65,132,25], [113,103,100,141,45]],
#                             [[53,112,100,141,45], [58,108,90,139,41], [65,104,80,139,33], [74,104,80,139,39], [84,104,80,139,39], [93,104,80,139,39], [103,104,80,139,30], [111,110,93,139,39]],
#                             [[57,120,103,177,66], [63,115,94,177,66], [69,111,84,177,61], [77,110,82,177,61], [86,110,82,177,61], [94,111,82,177,61], [102,111,86,175,55], [109,117,94,177,64]],
#                             [[62,125,116,180,64], [67,123,136,126,54], [74,121,126,44,124], [79,120,122,124,44], [87,120,122,124,44], [94,120,122,124,41], [102,121,125,124,41], [107,124,132,124,41]],
#                             [[66,138,172,115,52], [71,136,175,106,53], [76,131,161,106,48], [82,130,157,106,48], [88,130,157,106,48], [95,132,157,106,42], [101,132,157,106,40], [107,133,161,106,36]],
#                             [[69,146,179,158,76], [74,141,179,135,65], [79,140,179,135,73], [84,138,173,135,73], [90,138,173,135,73], [98,138,173,135,73], [101,142,171,145,75], [98,137,165,176,94]]]
        
        self.pawn_heights = read_from_json_file("pawn.json")
#         print(self.pawn_heights)
        
        self.tall_heights = read_from_json_file("tall.json")
#         print(self.pawn_heights)
        
#         self.other_heights = [[[28,98,85,94,17], [31,83,40,161,55], [34,74,38,134,33], [46,68,38,106,18], [63,65,37,98,21], [92,66,37,21,98], [112,83,57,98,21], [127,93,72,98,21]],
#                  [[38,106,102,83,6], [43,97,82,93,11], [51,92,72,93,11], [61,86,62,93,9], [76,87,62,93,9], [92,86,62,93,9], [107,92,72,93,9], [117,97,77,98,12]],
#                  [[47,107,102,12,98], [52,101,92,12,98], [58,97,82,12,98], [68,95,76,12,98], [81,95,77,12,98], [93,96,77,12,98], [104,100,85,12,98], [114,105,94,12,98]],
#                  [[54,111,114,12,98], [59,108,104,12,98], [64,104,95,12,98], [73,104,94,12,98], [84,102,93,12,98], [94,104,95,12,98], [104,107,100,12,98], [111,108,105,12,98]],
#                  [[57,116,128,104,22], [62,113,118,104,22], [69,113,113,104,22], [77,109,108,104,22], [85,110,107,104,22], [94,111,111,104,22], [102,113,113,104,22], [109,115,120,104,22]],
#                  [[62,123,142,116,38], [66,122,135,116,38], [73,120,130,116,38], [79,118,126,116,38], [87,118,126,116,38], [95,119,128,116,38], [101,119,129,116,38], [107,123,134,116,38]],
#                  [[66,134,163,126,48], [71,131,155,126,48], [76,129,148,126,48], [83,125,145,126,48], [88,125,140,126,48], [95,126,142,126,48], [101,127,145,126,48], [106,130,152,126,48]],
#                  [[69,146,180,180,97], [74,147,175,180,97], [79,141,168,180,97], [84,139,162,180,97], [89,138,160,180,97], [95,138,160,180,97], [100,144,166,180,97], [105,145,172,180,97]]]
#         
        self.other_heights = read_from_json_file("other.json")
        
        self.Q4 = [95, 97,114,172,100]
        
        
    def getValuesFromSquare(self, square, isPawn):
        #print(self.boardLabels)
        print(square)
        for i, row in enumerate(self.boardLabels):
            for j, val in enumerate(row):
                #print(val, i, j)
                if square == val:
                    if isPawn:
                        return self.pawn_heights[i][j]
                    else:
                        return self.other_heights[i][j]
                

            
class Robot():
    def __init__(self, startingAngle):
        self.m = RobotMath()
        self.chess = chessBoard()
        self.armMag = [0, 4.1, 4, 0, 0]
        self.armAngle = [95,86,230, 25, 50]
        self.basePosition = [5.2, -2, 4.2]
        self.A0 = [0,0,0]
        self.startingAngle = startingAngle
        self.currentAngle = [0,0,0,0,0]
        for i in range(len(startingAngle)):
            self.currentAngle[i] += startingAngle[i]
        self.controller = RobotController(self.currentAngle, self.armMag)
#         self.frame = RobotFrame()
#         self.armAnglerelative = self.frame.frameAngles()
#         print(self.chess.boardLabels)
#         print(len(self.chess.boardLabels))
        self.centerPosition = [90, 85, 101.0, 172, 105]
        self.origion1 = [179, 85, 101.0, 172, 105]
        self.origion2 = [179, 130, 91, 157, 120]

    def startingPosition(self):
#         print(self.startingAngle)
        self.controller.setStart(self.startingAngle)
        
    def returnMove(self):
        self.controller.servoMove(self.startingAngle)
        

    def Move(self, desiredAngle):
#         print(desiredAngle)
        self.controller.servoMove(desiredAngle)
        
  
        
    def moveSequence(self, position1, position2, isPawn):
        
        print("Moving ",position1," ", position2)
        print(self.chess.getValuesFromSquare(position1, isPawn))
        
        
        self.Move(self.centerPosition)
        sleep(1)
        print("Moved Center")
        
        if (position1[0] == "E" or position1[0] == "F" or position1[0] == "G" or position1[0] == "H"):
            if (position1[1] == "1" or position1[1] == "2" or position1[1] == "3" or position1[1] == "4"):
                #Q4
                self.Move(self.chess.Q4)
                sleep(1)
            else:
                self.Move(self.chess.Q4)
                sleep(1)
                #Q1
        else:
            if (position1[1] == "1" or position1[1] == "2" or position1[1] == "3" or position1[1] == "4"):
                self.Move(self.chess.Q4)
                sleep(1)
                #Q3
            else:
                self.Move(self.chess.Q4)
                sleep(1)
                #Q2           
        print("Moved Q")
        
#         p = self.chess.getValuesFromSquare('A5', True)
        self.Move(self.chess.getValuesFromSquare(position1, isPawn))
        sleep(1)
        self.EmagPull()
        sleep(2)
        self.Move(self.centerPosition)
        sleep(1)
        self.Move(self.chess.getValuesFromSquare(position2, isPawn))
        sleep(1)
        self.EmagPush()
        sleep(2)
        self.Move(self.centerPosition)
        sleep(1)
        self.EmagOff()
        sleep(2)
        self.Move(self.origion1)
        sleep(1)
        self.Move(self.origion2)
#         print(p)
        
                  
#     def headPosition(self):
#         YZ = self.frame.frameTotal(self.armMag, self.armAnglerelative)
#         print(YZ)
        
#     def setFrame(self):
#         A1 = self.frame.Arm(self.currentAngle[1], self.armAngle[1])
#         
#     def setBaseangle(self, desiredCoord):
#         f = self.setFrame(desiredCoord)
        
# class RobotFrame():
#     def __init__(self):
#         self.m = RobotMath()
# 
#     def frameAngles(self):
#         angle0 = 0
#         angle10 = 86
#         angle21 = angle10 + 125
#         angle32 = angle21 + 60
#         return [angle0, angle10,angle21,angle32]
#         
#     def Frame0(self,ang, mag):
#         y = self.m.frame0position(ang, mag)[0]
#         z = self.m.frame0position(ang, mag)[1]
#         return [y,z]
#     
#     def Frame1(self,ang, mag):
#         y = self.m.frame1position(ang, mag)[0]
#         z = self.m.frame1position(ang, mag)[1]
#         return [y,z]
#         
#     def Frame2(self,ang, mag):
#         y = self.m.frame2position(ang, mag)[0]
#         z = self.m.frame2position(ang, mag)[1]
#         return [y,z]
# 
#     def Frame3(self,ang, mag):
#         y = self.m.frame3position(ang, mag)[0]
#         z = self.m.frame3position(ang, mag)[1]
#         return [y,z]
#     
#     def frameTotal(self, mag, ang):
#         f0 = self.Frame0(ang[0], mag[0])
#         f1 = self.Frame1(ang[1], mag[1])
#         f2 = self.Frame2(ang[2], mag[2])
#         f3 = self.Frame3(ang[3], mag[3])
#         return [abs(f0[0]+f1[0]+f2[0]+f3[0]),f0[1]+f1[1]+f2[1]+f3[1]]
        

# self.currentAngle = [50, 150, 150,150]

# r = Robot([90, 80, 50,170])
# r.startingPosition()
# # desiredAngle = [90, 120, 120,120]
# # r.Move(desiredAngle)
# r.returnMove()
# r.headPosition()
    def EmagPull(self):
        GPIO.setup(12,GPIO.OUT) #pwm0
        GPIO.output(12,GPIO.HIGH)
        GPIO.setup(13,GPIO.OUT) #pwm1
        GPIO.output(13,GPIO.LOW)
        print("emag pulling hopefully")
    
    def EmagPush(self):
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,GPIO.LOW)
        GPIO.setup(13,GPIO.OUT)
        GPIO.output(13,GPIO.HIGH)
        print("emag pushing hopefully")
        
    def EmagOff(self):
        GPIO.setup(12,GPIO.OUT)
        GPIO.output(12,GPIO.LOW)
        GPIO.setup(13,GPIO.OUT)
        GPIO.output(13,GPIO.LOW)
        print("emag off hopefully")          
            
    
        
        
        