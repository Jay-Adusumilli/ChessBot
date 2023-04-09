import board, busio, adafruit_pca9685
from adafruit_servokit import ServoKit
import adafruit_motor.servo

class Communication():
    def __init__(self):
        self.i2c = board.I2C()
        self.pca = adafruit_pca9685.PCA9685(self.i2c)
        self.kit = ServoKit(channels = 16)
        self.pca.frequency = 50
#         self.servo0 = adafruit_motor.servo.Servo(0)
        
    def PCA(self, i, angle):
        self.kit.servo[i].angle = angle
#         self.servo0 = angle
 

class Pintext():
    def __init__(self):
        pass

    def Buildtext(self, pinNum):
        return ('Set Digital ' + str(pinNum) + ' ' + self.Buildinnercommand())
    
    def Buildinnercommand(self):
        raise NotImplementedError()
    
class Outputcommand(Pintext):
    def __init__(self, state1, state2):
        super().__init__()
        self.state1 = state1
        self.state2 = state2

    def Buildinnercommand(self):
        return (self.state1 + ' ' + self.state2)
    
class Inputcommand(Pintext):
    def __init__(self, state1):
        super().__init__()
        self.state1 = state1


    def Buildinnercommand(self):
        return (self.state1)
        
class Pins():
    def __init__(self, Pintext):
        self.GPIO = []
        Text = Pintext()
        for i in range(1,15):
            self.GPIO.append(i+13) 

    def Labelbuidler(self, **kwargs):
        if kwargs['first'] == 'Output':
            x = list(kwargs.values())
            command = Outputcommand(x[0], x[2])
            return command.Buildtext(x[1])
        else:
            x = list(kwargs.values())
            command = Inputcommand(x[0])
            response = command.Buildtext(x[1])
            return response
            
        

    def Pinlist(self):
        x = []
        for i in range(len(self.GPIO)):
            Pinstext = [str(self.GPIO[i])]
            x.append(Pinstext)
        return(x)
    

    def Setpins(self,num, IO, State):
        self.IOset(num,IO)
        if IO == 'Out':
            self.Output(num, State)
        else:
            self.Input(num)
            
            
    def IOset(self, num, IO):
        if IO == 'Out':
            GPIO.setup(num, GPIO.OUT)
        else:
            GPIO.setup(num, GPIO.IN)
            
    def Output(self, num, State):
        self.SetOutput(num)
#         print(num)
        if State == 'High':
            GPIO.output(num, GPIO.HIGH)
            print('Pin ' + str(num) + ' set ' + str(State))
        else:
            GPIO.output(num, GPIO.LOW)
            print('Pin ' + str(num) + ' set ' + str(State))
            
    def SetOutput(self, num):
        GPIO.setup(num, GPIO.OUT)
            
    def Input(self, num):
        GPIO.input(num)
        
        
                
#         
# p1 = Pins(Pintext)
# p1.Labelbuidler('Output', 'High')
# p1.Setpins(23, 'Out', 'l')
# 
#