import cv2
import numpy as np

# Define the colors of the chess pieces
colors = {'blue': [(100, 0, 0), (255, 50, 50)],
          'red': [(0, 0, 100), (50, 50, 255)]}

# Define the threshold for color detection
thresh = 50

# Initialize the webcam
cap = cv2.VideoCapture(0)

while True:
    # Read a frame from the webcam
    ret, img = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Apply a Gaussian blur to the image to reduce noise
    #blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    blurred = gray

    # Loop through each color and detect the pieces of that color
    for color, color_range in colors.items():
        # Create a mask for the color range
        lower = np.array(color_range[0])
        upper = np.array(color_range[1])
        mask = cv2.inRange(blurred, lower, upper)

        # Find contours in the mask
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Loop through each contour and check if it's a chess piece
        for cnt in contours:
            # Check if the contour is a chess piece by checking its area
            area = cv2.contourArea(cnt)
            if area > 100 and area < 2000:
                # Draw a bounding box around the chess piece
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(img, color + ' piece', (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Display the image with the chess pieces highlighted
    cv2.imshow('Chessboard Pieces', img)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()