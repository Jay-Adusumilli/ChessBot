import cv2
import numpy as np

# Create a VideoCapture object to capture images from the default camera
cap = cv2.VideoCapture(0)

# Check if camera opened successfully
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Read an image from the camera
ret, image = cap.read()

# Release the VideoCapture object
cap.release()

# Convert image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for red color
lower_red = np.array([30, 150, 150])
upper_red = np.array([40, 255, 255])

# Create masks for red color
mask = cv2.inRange(hsv, lower_red, upper_red)

# Apply mask to original image
red_objects = cv2.bitwise_and(image, image, mask=mask)

# Display result
cv2.imshow("Red Objects", red_objects)
cv2.waitKey(0)
cv2.destroyAllWindows()