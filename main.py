'''
This is the main file for the chess bot. It runs the GUI and the main loop.
The main loop calls the vision system and the UCI translation system.
The GUI is used to display the current state of the game and to allow the user to interact with the bot.
'''


# Imports.
import tkinter as tk
import tkinter.font as tkFont
from vision import vision
from UCI_Translation import Match
from PIL import ImageTk
from time import sleep


MAIN_LOOP_DELAY = 10                    # Control how fast the main loop runs (in ms).
CURRENT_STATE = "WATING TO START"       # The current state of the game.
STARTED = False                         # Whether the game has started or not.
PLAYER_TURN = True                      # Whether it is the player's turn or not.
PLAYER_SIDE = "w"                       # Whether the player is white or black.

ELO = 850                               # The bots ELO rating.
PATH_TO_STOCKFISH = "C:\\Users\\Jay\\Documents\\_Clemson\\Senior Design\\stockfish_15.1_win_x64_avx2.exe"     # The path to the stockfish executable.
MOVETIME = 5                           # The time the bot has to make a move (in seconds).

class App():
    def __init__(self, root):
        # Define Vars.
        App.message_info_box_msg = "Test\ntest"
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
        App.message_info_box.grid(row = 0, column = 1, pady = 10, padx=10)

        # Label.
        App.name_label=tk.Label(root)
        App.name_label["fg"] = "#333333"
        App.name_label["justify"] = "left"
        App.name_label["font"] = App.ft
        App.name_label["text"] = CURRENT_STATE
        #App.name_label.place(x=0,y=0,width=40,height=20)
        App.name_label.grid(row = 0, column = 0, pady = 10, padx=10)


        # Start button.
        App.start_game_button=tk.Button(root)
        App.start_game_button["bg"] = "#f0f0f0"
        App.start_game_button["font"] = App.ft
        App.start_game_button["fg"] = "#000000"
        App.start_game_button["justify"] = "left"
        App.start_game_button["text"] = "Start Game"
        #App.test_button.place(x=390,y=170,width=120,height=25)
        App.start_game_button.grid(row = 1, column = 0, pady = 10, padx=10)
        App.start_game_button["command"] = self.startGame

        # Switch sides button.
        App.switch_sides_button=tk.Button(root)
        App.switch_sides_button["bg"] = "#f0f0f0"
        App.switch_sides_button["font"] = App.ft
        App.switch_sides_button["fg"] = "#000000"
        App.switch_sides_button["justify"] = "left"
        App.switch_sides_button["text"] = "Switch Sides"
        #App.test_button.place(x=390,y=170,width=120,height=25)
        App.switch_sides_button.grid(row = 2, column = 0, pady = 10, padx=10)
        App.switch_sides_button["command"] = self.switchSides

        # End move button.
        App.end_move_button=tk.Button(root)
        App.end_move_button["bg"] = "#f0f0f0"
        App.end_move_button["font"] = App.ft
        App.end_move_button["fg"] = "#000000"
        App.end_move_button["justify"] = "left"
        App.end_move_button["text"] = "End Move"
        #App.test_button.place(x=390,y=170,width=120,height=25)
        App.end_move_button.grid(row = 3, column = 0, pady = 10, padx=10)
        App.end_move_button["command"] = self.endMove

    # Start the game.
    def startGame(self):
        STARTED = True
        if PLAYER_SIDE == "w":
            PLAYER_TURN = True
        else:
            PLAYER_TURN = False

    # Switch which side the player is on.
    def switchSides(self):
        if PLAYER_SIDE == "w":
            PLAYER_SIDE = "b"
        elif PLAYER_SIDE == "b":
            PLAYER_SIDE = "w"

    # End the player's turn.
    def endMove(self):
        PLAYER_TURN = False
    
    # Update the text in the message box.
    def update_window(self):
        App.message_info_box["text"] = App.message_info_box_msg

    # Update the text in the message box.
    def updateText(self, msg):
        App.message_info_box_msg = msg
        self.update_window()

    
# The main loop that runs after the GUI loop.
def mainLoop(root, v, app, stock):

    # Get the most up to date board.
    vision_board = v.update()

    # Update the text for debugging.
    visionboardprint = ""
    for i, j in enumerate(vision_board):
        visionboardprint = visionboardprint + str(vision_board[i]) + "\n"
    app.updateText(str(visionboardprint))


    if STARTED != True:                         # Waiting to start.
        CURRENT_STATE = "WATING TO START"
    elif PLAYER_TURN == True:                   # Player's turn, just wait.
        CURRENT_STATE = "PLAYER TURN"
    elif PLAYER_TURN == False:                  # Computer's turn, run through the steps to make a move.
        CURRENT_STATE = "COMPUTER TURN"
        # TODO: 
        # Send the current board state to the UCI translation system and get the moves out.
        #stock.playerMove(vision_board)
        #stock.displayBoard()                   # Display the board for debugging.
        #move = stock.stockFishMove()            # Get the move from stockfish.

        # Send the list of moves to the arm.

        # Wait for the arm to finish moving.

        # Reset the vars to the player state.
        sleep(2000)
        PLAYER_TURN = True
    

    # Call this function again until the GUI is closed.
    root.after(MAIN_LOOP_DELAY, mainLoop, root, v, app, stock)




# Run the main loop.
if __name__ == "__main__":
    stock = Match(ELO, 15, PATH_TO_STOCKFISH, MOVETIME)            # Initialize the UCI translation system and stockfish.
    #stock = 0
    v = vision(True)                                                # Initialize and run the computer vision.
    root = tk.Tk()                                                  # Start the HID app.
    app = App(root)
    root.after(MAIN_LOOP_DELAY, mainLoop, root, v, app, stock)     # Run the main loop after starting the GUI.
    root.mainloop()                                                 # Start the GUI.
    v.shutdown()                                                    # Shutdown the vision system and tabs.