from tkinter    import ttk, Tk, Button, Label, Entry, PhotoImage, Frame, Toplevel, OptionMenu, StringVar
from MotorSetup import Robot
from Pi_Setup import Pins, Pintext
import RPi.GPIO as GPIO
import json
GPIO.setmode(GPIO.BCM)

GPIO.setwarnings(False)


class ChessBot(Tk):
    
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #containter contains stuff to populate
        container = Frame(self, bg='white')
        container.pack(side="top", fill="both", expand = True)
#         container.grid_rowconfigure(0, weight=1)
#         container.grid_columnconfigure(0, weight=1)
        self.title('ChessBot')
        self.frames = {}
#         self.geometry("700x350")
        
        for F in (StartPage, MotorPage):
            #anything ALL frames needs should be here
            frame = F(container, self, Pins)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
            
        frame.grid(row=0,column=0,sticky="nsew")
        self.show_frame(StartPage)
     
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        
class StartPage(Frame):
    def __init__(self, parent, controller, Pins):
        Frame.__init__(self,parent)
#         label = Label(self, text = "Start Page")
#         label.grid(row=0,column=0, padx=10)#(pady=10, padx=10)

        FrameList = [["Go to MotorPage"], [lambda: controller.show_frame(MotorPage)]]
        for i in range(len(FrameList[0])):
            Button(self, text = FrameList[0][i], command = FrameList[1][i]).grid(row=0+i,column=0)

        
        
class MotorPage(Frame):
    def __init__(self, parent, controller, Pins):
        
        Frame.__init__(self,parent)
        self.Text = Pintext
        self.Pins = Pins(self.Text)
        self.Pinnum = [0, 0, 0]
        self.Digitalpins = ['Output High', 'Output Low', 'Input']
        self.Digitalset = ['Output High', 'Output Low', 'Input']
#         print(self.Digitalpins[0].split())
        
        self.motorNum = ['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4', 'Motor 5']
        self.motorVal = [0,0,0,0,0]
        self.temprow = [[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
        pins = self.Pins.Pinlist()
        outhigh = []
        outlow = []
        inputlabel = []
        startingAngle = [179, 130, 91, 157, 120]
        self.currentAngle = [179, 130, 91, 157, 120]
        self.robot = Robot(startingAngle)
        self.robot.startingPosition()
#         print(self.robot.chess.boardLabels)
#         print(self.robot.chess.boardLabels[7][7][0])
#         print(self.robot.chess.pawn_heights[7][7])
#         self.robot.movePiece()
#         ang = self.heightVal([0,0,0,0,0])
        
        
        for i in range(len(self.Digitalpins)):
            self.GPIOlist(i)
            
        for i in range(len(self.currentAngle)):
            self.motorList(i)
            
        Button(self, text = 'Origin', command = lambda : self.originMove()).grid(row =0,column=8)
            
        Button(self, text = 'Center', command = lambda : self.centerMove()).grid(row =1,column=8)
        
        Button(self, text = 'EmagPull', command = lambda : self.EmagPull()).grid(row = 2, column = 8)
        Button(self, text = 'EmagPush', command = lambda : self.EmagPush()).grid(row = 3, column = 8)
        Button(self, text = 'EmagOff', command = lambda : self.EmagOff()).grid(row = 4, column = 8)
#         Button(self, text = 'Test', command = lambda : self.test()).grid(row = 5, column = 8)
        Button(self, text = 'Set Pawn Heights', command = lambda : self.pawnHeightset()).grid(row = 0, column = 9)
        Button(self, text = 'Set Other Heights', command = lambda : self.otherHeightset()).grid(row = 1, column = 9)
        Button(self, text = 'Set Tall Heights', command = lambda : self.tallHeightset()).grid(row = 2, column = 9)
        Button(self, text = 'Test Pawn Heights', command = lambda : self.pawnHeightcheck()).grid(row = 0, column = 10)
        Button(self, text = 'Test Other Heights', command = lambda : self.otherHeightcheck()).grid(row = 1, column = 10)
        Button(self, text = 'Test Tall Heights', command = lambda : self.tallHeightcheck()).grid(row = 2, column = 10)
                
#         for i in range (2):
#             for j in range(3):
#                 Button(self, image=Circle, command = self.funcLambda(i, j)).grid(row=i+1 ,column=j)
    
    def setAngle(self):
        ang = [0,0,0,0,0]
        for i in range(len(ang)):
            ang[i] += self.currentAngle[i]
        return ang
    
    def curAngle(self, ang):
        self.currentAngle=[0,0,0,0,0]
        for i in range(len(ang)):
            self.currentAngle[i] += ang[i]


    def write_to_pawn_json_file(self, i, j, data):
        self.robot.chess.pawn_heights[i][j] = data
        with open("pawn.json", 'w') as f:
            json.dump(self.robot.chess.pawn_heights, f)
            
    def write_to_other_json_file(self,i, j, data):
        self.robot.chess.other_heights[i][j] = data
        with open("other.json", 'w') as f:
            json.dump(self.robot.chess.other_heights, f)

    def write_to_tall_json_file(self, i, j, data):
        self.robot.chess.tall_heights[i][j] = data
        with open("tall.json", 'w') as f:
            json.dump(self.robot.chess.tall_heights, f)

    def checkPawnheight(self):
        print(self.robot.chess.pawn_heights[7][7])
        
    def test(self):
        self.robot.moveSequence('H1', 'E4', True)

    def pawnHeightset(self):
        top = Toplevel()
        top.title('Set Pawn Height')
        for i, row in enumerate(self.robot.chess.boardLabels):
            for j, val in enumerate(row):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = self.lambdaPawnset(i,j)).grid(row=i ,column=j)
        
    def otherHeightset(self):
        top = Toplevel()
        top.title('Set Other Height')
        for i in range(len(self.robot.chess.boardLabels)):
            for j in range(len(self.robot.chess.boardLabels)):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = lambda : self.lambdaOtherset(i,j)).grid(row=i+1 ,column=j)
                
    def tallHeightset(self):
        top = Toplevel()
        top.title('Set Tall Height')
        for i in range(len(self.robot.chess.boardLabels)):
            for j in range(len(self.robot.chess.boardLabels)):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = lambda : self.lambdaTallset(i,j)).grid(row=i+1 ,column=j)
                
    def lambdaPawnset(self, i, j):
        return lambda : self.setPawnheight(i,j)
    
    def lambdaOtherset(self, i, j):
        return lambda : self.setOtherheight(i,j)
    
    def lambdaTallset(self, i, j):
        return lambda : self.setTallheight(i,j)
    
    def setPawnheight(self, i, j):
        ang = self.setAngle()
        self.write_to_pawn_json_file(i,j,ang)
#         curAng = self.curAngle(ang)
        print(self.robot.chess.pawn_heights)
        
    def setOtherheight(self, i, j):
        ang = self.setAngle()
        self.write_to_other_json_file(i,j,ang)
        print(self.robot.chess.other_heights)
        
    def setTallheight(self, i, j):
        ang = self.setAngle()
        self.write_to_tall_json_file(i,j,ang)
        print(self.robot.chess.tall_heights)
        
    def pawnHeightcheck(self):
        top = Toplevel()
        top.title('Check Pawn Height')
        for i, row in enumerate(self.robot.chess.boardLabels):
            for j, val in enumerate(row):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = self.lambdaPawncheck(i,j)).grid(row=i ,column=j)
                
    def otherHeightcheck(self):
        top.title('Check Other Height')
        top = Toplevel()
        for i, row in enumerate(self.robot.chess.boardLabels):
            for j, val in enumerate(row):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = self.lambdaOthercheck(i,j)).grid(row=i ,column=j)
                
    def tallHeightcheck(self):
        top.title('Check Tall Height')
        top = Toplevel()
        for i, row in enumerate(self.robot.chess.boardLabels):
            for j, val in enumerate(row):
                Button(top, text = self.robot.chess.boardLabels[i][j], command = self.lambdaTallcheck(i,j)).grid(row=i ,column=j)
                
    def lambdaPawncheck(self, i, j):
        return lambda : self.checkPawnheight(i,j)
    
    def lambdaOthercheck(self, i, j):
        return lambda : self.checkPawnheight(i,j)
    
    def lambdaTallcheck(self, i, j):
        return lambda : self.checkPawnheight(i,j)
    
    def checkPawnheight(self, i,j):
        self.curAngle(self.robot.chess.pawn_heights[i][j])
        self.robot.Move(self.robot.chess.pawn_heights[i][j])
        
    def checkTallheight(self, i,j):
        self.robot.Move(self.robot.chess.tall_heights[i][j])
        
    def checkOtherheight(self, i,j):
        self.robot.Move(self.robot.chess.other_heights[i][j])
           
    def setOtherheight(self, i, j):
        self.robot.chess.other_heights[i][j] = self.currentAngle
        write_to_json_file(self.robot.chess.other_heights, "other.json")
        
    def setTallheight(self, i, j):
        self.robot.chess.tall_heights[i][j] = self.currentAngle
        write_to_json_file(self.robot.chess.tall_heights, "tall.json")
            
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
        
    def GPIOlist(self, i):
        Label(self, text = self.Digitalpins[i], fg="black", bg="white", width = 10).grid(row=i,column = 0)
        self.Pinnum[i] = Entry(self, fg="black", bg="white", width=5)
        self.Pinnum[i].grid(row=i, column=1)
        Button(self, text = 'Set', command = lambda : self.GPIOset(i)).grid(row =i,column=2)
        
    def motorList(self, i):
        Button(self, text = '-5', command = lambda : self.ccwServo_m5(i)).grid(row =i,column=3)
        Button(self, text = '-1', command = lambda : self.ccwServo_m1(i)).grid(row =i,column=4)
        Label(self, text = self.motorNum[i], fg="black", bg="white", width = 10).grid(row=i,column = 5)
        Button(self, text = '+1', command = lambda : self.cwServo_p1(i)).grid(row =i,column=6)
        Button(self, text = '+5', command = lambda : self.cwServo_p5(i)).grid(row =i,column=7)
        
    def ccwServo_m5(self, i):
        self.currentAngle[i] -= 5
        self.robot.Move(self.currentAngle)
        
    def ccwServo_m1(self, i):
#         ang = self.setAngle()
        self.currentAngle[i] -= 1
        self.robot.Move(self.currentAngle)
    
    def cwServo_p1(self, i):
#         ang = self.setAngle()
        self.currentAngle[i] += 1
        self.robot.Move(self.currentAngle)
        
    def cwServo_p5(self, i):
#         ang = self.setAngle()
        self.currentAngle[i] += 5
        self.robot.Move(self.currentAngle)
        
    def GPIOset(self, i):
        if i == 0:
            x = self.Digitalpins[i].split()
            self.Pins.Output(int(self.Pinnum[i].get()), x[1])
        if i == 1:
            x = self.Digitalpins[i].split()
            self.Pins.Output(int(self.Pinnum[i].get()), x[1])
        if i == 2:
            self.Pins.Output(i)
            
    def originMove(self):
        self.currentAngle = [179, 85, 101.0, 172, 105]
        self.robot.Move(self.currentAngle)
        self.currentAngle = [179, 130, 91, 157, 120]
        self.robot.Move(self.currentAngle)
        
    def centerMove(self):
        self.currentAngle = [90, 85, 101.0, 172, 105]
        self.robot.Move(self.currentAngle)
        
 
#         for i in range(len(pins)):
#             for j in (1,2,3):
#                 if j == 1:
#                     outhigh.append(self.Pins.Labelbuidler(first = 'Output', second = pins[i], third = 'High'))
#                 if j == 2:
#                     outlow.append(self.Pins.Labelbuidler(first = 'Output', second = pins[i], third = 'Low'))
#                     
#                 else:
#                     inputlabel.append(self.Pins.Labelbuidler(first = 'Input', second = pins[i]))
# 
#         for i in range(len(pins)):
#             for j in (1,2,3):
#                 if j == 1:
#                     Button(self, text = outhigh[i], command = lambda : self.Output(i, j)).grid(row =i,column=j)
#                 if j == 2:
#                     Button(self, text = outlow[i], command = lambda : self.Output(i, j)).grid(row =i,column=j+1)
#                 else:
#                     Button(self, text = inputlabel[i], command = lambda : self.Output(i, j)).grid(row =i,column=j+2)
# 
# 
#         def Output(self, i, j):
#             if j == 1:   
#                 self.Pins.Setpins(i, 'Out', 'High')
#             if j == 2:
#                 self.Pins.Setpins(i, 'Out', 'Low')
#             else:
#                 self.Pins.Setpins(i, 'Out', 'Low')
    


                    
if __name__=="__main__":
    app = ChessBot()
    app.mainloop()
        
         