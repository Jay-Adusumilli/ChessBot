import cv2
import numpy as np
from time import sleep

# Define the dimensions of the chessboard
rows = 8
cols = 8

# Define the size of each square in pixels
square_size = 50

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:

    #sleep(.5)

    num_coutours = 0

    # Read a frame from the webcam
    ret, img = cap.read()

    # Convert frame to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Convert the frame to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)

    # Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (3, 3), 10)
    #cv2.imshow('blurred', blurred)

    # Kernel to sharpen the image.
    #sharpen_kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    #sharp = cv2.filter2D(gray, -1, sharpen_kernel)
    #cv2.imshow('sharpened', sharp)


    # Find the edges in the image using Canny edge detection

    edges = cv2.Canny(blurred, 40, 150, apertureSize=3)

    # Find the contours of the edges
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw a box around every square on the chessboard
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 800:
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
            if len(approx) == 4:
                num_coutours += 1
                x, y, w, h = cv2.boundingRect(approx)
                if w > 0.7 * square_size and h > 0.7 * square_size and w < 1.3 * square_size and h < 1.3 * square_size:
                    pass
                    #cv2.putText(img, str(num_coutours), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                    #cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            elif len(approx) > 2:
                x, y, w, h = cv2.boundingRect(approx)
                cv2.putText(img, "piece", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Display the image with the chessboard highlighted
    cv2.putText(img, str(num_coutours), (575,35), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0))
    
    cv2.imshow('edges', edges)
    cv2.imshow('Chessboard', img)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()