from tkinter    import ttk, Tk, Button, Label, Entry, PhotoImage, Frame, Toplevel, OptionMenu, StringVar
from MotorSetup import Robot
from Pi_Setup import Pins, Pintext


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
        
        self.motorNum = ['Motor 1', 'Motor 2', 'Motor 3', 'Motor 4']
        self.motorVal = [0,0,0,0]
        

        pins = self.Pins.Pinlist()
        outhigh = []
        outlow = []
        inputlabel = []
        startingAngle = [90, 80, 30,120]
        self.currentAngle = [90, 80, 30,120]
        self.robot = Robot(startingAngle)
        self.robot.startingPosition()
        
        for i in range(len(self.Digitalpins)):
            self.GPIOlist(i)
            
        for i in range(len(self.currentAngle)):
            self.motorList(i)
        
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
        self.currentAngle[i] = self.currentAngle[i]-5
        self.robot.Move(self.currentAngle)
        
    def ccwServo_m1(self, i):
        self.currentAngle[i] = self.currentAngle[i]-1
        self.robot.Move(self.currentAngle)
    
    def cwServo_p1(self, i):
        self.currentAngle[i] = self.currentAngle[i]+1
        self.robot.Move(self.currentAngle)
        
    def cwServo_p5(self, i):
        self.currentAngle[i] = self.currentAngle[i]+5
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
    


'''
if __name__=="__main__":
    app = ChessBot()
    app.mainloop()
'''