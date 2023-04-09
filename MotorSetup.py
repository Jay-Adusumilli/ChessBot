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


GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


# factory = PiGPIOFactory()
# 
# servo1 = Servo(12, min_pulse_width=0.125/1000, max_pulse_width=.725/1000, pin_factory=factory)
# servo2 = Servo(13, min_pulse_width=0.13/1000, max_pulse_width=0.6/1000, pin_factory=factory)



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
        currentAngle += .25
        self.controller.PCA(i, currentAngle)
        return currentAngle
        
    def CW(self, i, currentAngle):
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
        self.Arms = [Arm(Armlength[0], self.servoDirection, ), Arm(Armlength[1], self.servoDirection), Arm(Armlength[2], self.servoDirection), Arm(Armlength[3], self.servoDirection)] 
         
    def numberServos(self, desiredAngle):
        servoNum = list(range(4))
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
        print(self.currentAngle)
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
            sleep(.0025)
            
class RobotFrame():
    def __init__(self):
        self.m = RobotMath()

    def frameAngles(self):
        angle0 = 0
        angle10 = 86
        angle21 = angle10 + 125
        angle32 = angle21 + 60
        return [angle0, angle10,angle21,angle32]
        
    def Frame0(self,ang, mag):
        y = self.m.frame0position(ang, mag)[0]
        z = self.m.frame0position(ang, mag)[1]
        return [y,z]
    
    def Frame1(self,ang, mag):
        y = self.m.frame1position(ang, mag)[0]
        z = self.m.frame1position(ang, mag)[1]
        return [y,z]
        
    def Frame2(self,ang, mag):
        y = self.m.frame2position(ang, mag)[0]
        z = self.m.frame2position(ang, mag)[1]
        return [y,z]

    def Frame3(self,ang, mag):
        y = self.m.frame3position(ang, mag)[0]
        z = self.m.frame3position(ang, mag)[1]
        return [y,z]
    
    def frameTotal(self, mag, ang):
        f0 = self.Frame0(ang[0], mag[0])
        f1 = self.Frame1(ang[1], mag[1])
        f2 = self.Frame2(ang[2], mag[2])
        f3 = self.Frame3(ang[3], mag[3])
        return [abs(f0[0]+f1[0]+f2[0]+f3[0]),f0[1]+f1[1]+f2[1]+f3[1]]
    

            
class Robot():
    def __init__(self, startingAngle):
        self.m = RobotMath()
        self.armMag = [0, 4.1, 4, 0]
        self.armAngle = [95,86,230, 25]
        self.basePosition = [5.2, -2, 4.2]
        self.A0 = [0,0,0]
        self.startingAngle = startingAngle
        self.currentAngle = [0,0,0,0]
        for i in range(len(startingAngle)):
            self.currentAngle[i] += startingAngle[i]
        self.controller = RobotController(self.currentAngle, self.armMag)
        self.frame = RobotFrame()
        self.armAnglerelative = self.frame.frameAngles()
        print(self.armAnglerelative)

        
    def startingPosition(self):
        print(self.startingAngle)
        self.controller.setStart(self.startingAngle)
        
    def returnMove(self):
        self.controller.servoMove(self.startingAngle)
        

    def Move(self, desiredAngle):
        self.controller.servoMove(desiredAngle)
        
                  
    def headPosition(self):
        YZ = self.frame.frameTotal(self.armMag, self.armAnglerelative)
        print(YZ)
        
    def setFrame(self):
        A1 = self.frame.Arm(self.currentAngle[1], self.armAngle[1])
        
    def setBaseangle(self, desiredCoord):
        f = self.setFrame(desiredCoord)
        

# self.currentAngle = [50, 150, 150,150]

# r = Robot([90, 80, 30,120])
# r.startingPosition()
# desiredAngle = [90, 120, 120,120]
# r.Move(desiredAngle)
# r.returnMove()
# r.headPosition()
        
            
    
        
        
        