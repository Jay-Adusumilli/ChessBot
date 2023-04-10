import cv2
import numpy as np
from time import sleep

class vision:
    def __init__(self, show_image):
        vision.rows = 8
        vision.cols = 8
        vision.cap = cv2.VideoCapture(0)
        vision.show_image = show_image
    
    # Get the current image and output the board state.
    def update(self):
        vision.board = []
        ret, img = vision.cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (3, 3), 10)
        edges = cv2.Canny(blurred, 40, 150, apertureSize=3)

        if vision.show_image == True:
            cv2.imshow('edges', edges)
            cv2.imshow('Chessboard', img)
        return vision.board
    
    def shutdown(self):
        vision.cap.release()
        cv2.destroyAllWindows()

v = vision(True)
while 1:
    try:
        v.update()
    except KeyboardInterrupt:
        break

v.shutdown()
