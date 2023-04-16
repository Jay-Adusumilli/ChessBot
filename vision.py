import cv2
import numpy as np

class vision:
    # Initialize the class.
    def __init__(self, show_image):

        # Define an empty board.
        vision.board = [['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],]
        
        vision.board_positions = [[[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]],
                                [[0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]]]
        
        # +- Value
        vision.bounds = 30

        # Define colors.
        #vision.red_color = [10, 60.5, 76.5]
        #vision.blue_color = [218, 60.3, 98.8]
        vision.green_color = [157, 39.5, 48.6]
        vision.yellow_color = [58, 78.6, 87.8]
        vision.orange_color = [23, 63.2, 99.2]
        #vision.pink_color = [332, 52.1, 94.1]
        # Lower bounds.
        vision.red_color_lower = [30, 150, 50]
        vision.blue_color_lower = [150, 217, 165]
        vision.green_color_lower = [x - vision.bounds for x in vision.green_color]
        vision.yellow_color_lower = [x - vision.bounds for x in vision.yellow_color]
        vision.orange_color_lower = [x - vision.bounds for x in vision.orange_color]
        vision.pink_color_lower = [140, 170, 50]
        # Upper bounds.
        vision.red_color_upper = [255, 255, 180]
        vision.blue_color_upper = [157, 193, 160]
        vision.green_color_upper = [x + vision.bounds for x in vision.green_color]
        vision.yellow_color_upper = [x + vision.bounds for x in vision.yellow_color]
        vision.orange_color_upper = [x + vision.bounds for x in vision.orange_color]
        vision.pink_color_upper = [177, 255, 255]
        
        



        # Define masks for each color.
        # Color: [Lower, Upper] bounds. (HSV values).
        vision.color_ranges = {
            "red": [np.array(vision.red_color_lower).astype(np.uint8), np.array(vision.red_color_upper).astype(np.uint8)],
            "blue": [np.array(vision.blue_color_lower).astype(np.uint8), np.array(vision.blue_color_upper).astype(np.uint8)],
            "green": [np.array(vision.green_color_lower).astype(np.uint8), np.array(vision.green_color_upper).astype(np.uint8)],
            "yellow": [np.array(vision.yellow_color_lower).astype(np.uint8), np.array(vision.yellow_color_upper).astype(np.uint8)],
            "orange": [np.array(vision.orange_color_lower).astype(np.uint8), np.array(vision.orange_color_upper).astype(np.uint8)],
            "pink": [np.array(vision.pink_color_lower).astype(np.uint8), np.array(vision.pink_color_upper).astype(np.uint8)]
        }

        # Start the webcam.
        vision.cap = cv2.VideoCapture(0)
        vision.show_image = show_image

    
    # Get the current image and output the board state.
    def update(self):
        # Reset the board.
        vision.board = [['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],
                        ['-', '-', '-', '-', '-', '-', '-', '-'],]
        
        # Get an image frame.
        ret, img = vision.cap.read()
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #blurred = cv2.GaussianBlur(gray, (3, 3), 10)
        #edges = cv2.Canny(blurred, 40, 150, apertureSize=3)

        vision.color_masks = {}

        for color in vision.color_ranges:
            vision.color_masks[color] = cv2.inRange(hsv, vision.color_ranges[color][0], vision.color_ranges[color][1])
            blurred = cv2.GaussianBlur(vision.color_masks[color], (3, 3), 10)
            edges = cv2.Canny(blurred, 40, 150, apertureSize=3)
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 200:
                    perimeter = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
                    if len(approx) > 5:
                        x, y, w, h = cv2.boundingRect(approx)
                        cv2.putText(img, color, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            

        cv2.imshow("pink", vision.color_masks["pink"])
        cv2.imshow("blue", vision.color_masks["blue"])
        #cv2.imshow("blurred",blurred)
        #cv2.imshow("edges", edges)
        cv2.imshow("Original", img)
        return vision.board
    
    def shutdown(self):
        vision.cap.release()
        cv2.destroyAllWindows()

'''
v = vision(True)
while 1:
    v.update()
    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        v.shutdown()
        break

v.shutdown()
'''
