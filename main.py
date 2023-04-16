import tkinter as tk
import tkinter.font as tkFont
from vision import vision
from cv2 import waitKey
from time import sleep

# Control how fast the main loop runs.
MAIN_LOOP_DELAY = 10



class App():
    def __init__(self, root):
        # Define Vars.
        App.message_info_box_msg = "Test"
        # Set title.
        root.title("Chess Bot")
        # Adjust window.
        width=1200
        height=800
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)

        # App font.
        App.ft = tkFont.Font(family='Times',size=14)

        # Main message box.
        App.message_info_box=tk.Message(root)
        App.message_info_box["font"] = App.ft
        App.message_info_box["fg"] = "#333333"
        App.message_info_box["justify"] = "left"
        App.message_info_box["text"] = App.message_info_box_msg
        #App.message_info_box.place(x=0,y=0,width=40,height=20)
        App.message_info_box.grid(row = 1, column = 0, pady = 10, padx=10)

        # Button code.
        App.test_button=tk.Button(root)
        App.test_button["bg"] = "#f0f0f0"
        App.test_button["font"] = App.ft
        App.test_button["fg"] = "#000000"
        App.test_button["justify"] = "center"
        App.test_button["text"] = "Adjust Colors"
        #App.test_button.place(x=390,y=170,width=120,height=25)
        App.test_button.grid(row = 0, column = 0, pady = 10, padx=10)
        App.test_button["command"] = self.calibrateColors

    def test_button_command(self):
        pass
    
    def update_window(self):
        App.message_info_box["text"] = App.message_info_box_msg

    def calibrateColors(self):
        App.color_window = tk.Toplevel(root)
        App.color_window.title = "Color Calibration"
        App.color_window.geometry("600x400")
        App.h_label = tk.Label(App.color_window, text = "H", font = App.ft).grid(row=1,column=0, pady = 10, padx=10)
        App.s_label = tk.Label(App.color_window, text = "S", font = App.ft).grid(row=2,column=0, pady = 10, padx=10)
        App.v_label = tk.Label(App.color_window, text = "V", font = App.ft).grid(row=3,column=0, pady = 10, padx=10)
        App.red_label = tk.Label(App.color_window, text = "red", font = App.ft).grid(row=0,column=1, pady = 10, padx=10)
        App.blue_label = tk.Label(App.color_window, text = "blue", font = App.ft).grid(row=0,column=2, pady = 10, padx=10)
        App.green_label = tk.Label(App.color_window, text = "green", font = App.ft).grid(row=0,column=3, pady = 10, padx=10)
        App.yellow_label = tk.Label(App.color_window, text = "yellow", font = App.ft).grid(row=0,column=4, pady = 10, padx=10)
        App.orange_label = tk.Label(App.color_window, text = "orange", font = App.ft).grid(row=0,column=5, pady = 10, padx=10)
        App.pink_label = tk.Label(App.color_window, text = "pink", font = App.ft).grid(row=0,column=6, pady = 10, padx=10)


# The main loop that runs after the GUI loop.
def mainLoop(root, v, app):

    v.update()
    # Call this function again until the GUI is closed.
    root.after(MAIN_LOOP_DELAY, mainLoop, root, v)




# Run the main loop.
if __name__ == "__main__":

    v = vision(True)                                # Initialize and run the computer vision.

    root = tk.Tk()                                  # Start the HID app.
    app = App(root)

    root.after(MAIN_LOOP_DELAY, mainLoop, root, v, app)  # Run the main loop after starting the GUI.
    root.mainloop()                                 # Start the GUI.
    
    v.shutdown()                                    # Shutdown the vision system and tabs.