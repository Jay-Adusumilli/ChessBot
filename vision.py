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
        
        # Define a list of center points of the board postions.
        # Ignore values in here for now.
        vision.board_positions = [[[167,105], [461,105], [528,105], [592,105], [660,105], [724,105], [792,105], [859,105]],
                                [[167,143], [463,143], [527,143], [594,143], [661,143], [727,143], [792,143], [863,143]],
                                [[167,180], [465,180], [530,180], [597,180], [662,180], [732,180], [800,180], [865,180]],
                                [[167,218], [465,218], [530,218], [597,304], [662,304], [732,304], [800,304], [865,304]],
                                [[167,368], [465,368], [530,368], [597,368], [662,368], [732,368], [800,368], [865,368]],
                                [[167,436], [465,436], [530,436], [597,436], [662,436], [732,436], [800,436], [865,436]],
                                [[167,504], [465,504], [530,504], [597,504], [662,504], [732,504], [800,504], [865,504]],
                                [[167,570], [465,570], [530,570], [597,570], [662,570], [732,570], [800,570], [865,570]]]
        

        # Define the top left center of the board and how far the boxes are from each other.
        top_left = [167, 105]
        dist = 38
        y = top_left[1]
        for i in vision.board_positions:
            x = top_left[0]
            for j in i:
                j[0] = x
                j[1] = y
                x += dist
            y += dist

        vision.board_edges = [[top_left[0]-dist-5,top_left[1]-dist-5], [top_left[0] + dist * 8 + 5, top_left[1] + dist * 8 + 5]]

        # How far to look from the center of the square.
        vision.radius = 8

        # Map the colors to a piece on the board.
        vision.color_map = {
            "red": "p",
            "blue": "r",
            "green": "n",
            "yellow": "b",
            "orange": "q",
            "pink": "k"
            }
        
        
        # +- Value
        vision.bounds = 30

        # Define colors.
        #vision.red_color = [10, 60.5, 76.5]
        #vision.blue_color = [218, 60.3, 98.8]
        #vision.green_color = [157, 39.5, 48.6]
        #vision.yellow_color = [58, 78.6, 87.8]
        #vision.orange_color = [23, 63.2, 99.2]
        #vision.pink_color = [332, 52.1, 94.1]
        # Lower bounds.
        vision.red_color_lower = [0, 50, 50]
        vision.blue_color_lower = [90, 140, 140]
        vision.green_color_lower = [65, 70, 70]
        vision.yellow_color_lower = [20, 100, 100]
        vision.orange_color_lower = [10, 50, 50]
        vision.pink_color_lower = [155, 50, 50]
        # Upper bounds.
        vision.red_color_upper = [10, 255, 255]
        vision.blue_color_upper = [120, 255, 255]
        vision.green_color_upper = [90, 255, 220]
        vision.yellow_color_upper = [50, 255, 255]
        vision.orange_color_upper = [20, 255, 255]
        vision.pink_color_upper = [180, 255, 255]
        
        vision.lower_red2 = np.array([170, 50, 50])
        vision.upper_red2 = np.array([180, 255, 255])



        # Define masks for each color.
        # Color: [Lower, Upper, Piece] bounds. (HSV values).
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

        # Draw dots on the board corners.
        cv2.circle(img, (vision.board_edges[0][0], vision.board_edges[0][1]), radius=1, color=(0, 255, 0), thickness=-1)
        cv2.circle(img, (vision.board_edges[1][0], vision.board_edges[1][1]), radius=1, color=(0, 255, 0), thickness=-1)
        cv2.circle

        vision.color_masks = {}
        vision.found_black = []         # [X, Y, R, color]
        vision.found_white = []         # [X, Y, R, color]

        # Loop through all colors and find colored circles and rectangles.
        for color in vision.color_ranges:
            vision.color_masks[color] = cv2.inRange(hsv, vision.color_ranges[color][0], vision.color_ranges[color][1])  # Make a mask using the color range given.
            if color == "red":
                mask2 = cv2.inRange(hsv, vision.lower_red2, vision.upper_red2)
                vision.color_masks[color] = cv2.bitwise_or(vision.color_masks[color], mask2)
            
            #blurred = cv2.GaussianBlur(vision.color_masks[color], (3, 3), 10)                                           # Blur the image to improve the contours.
            kernel = np.ones((5,5), np.uint8)
            morph = cv2.morphologyEx(vision.color_masks[color], cv2.MORPH_CLOSE, kernel)                                # Fill in the gaps to imporove contours.
            edges = cv2.Canny(morph, 10, 200, apertureSize=3)                                                           # Find canny edges.
            contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)                       # Get list of contours.
            # Loop through all countours.
            for contour in contours:
                area = cv2.contourArea(contour)                                                                         # Get the area of the contour and move on if its >200.
                if area > 200 and area < 1000:
                    # Get the number of lines in the polygon detetcted.
                    perimeter = cv2.arcLength(contour, True)
                    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
                    # If a circle is found.
                    if len(approx) > 3:
                        # Draw a circle around the circle found.
                        (x, y), radius = cv2.minEnclosingCircle(contour)
                        center = (int(x), int(y))
                        radius = int(radius)
                        if x > vision.board_edges[0][0] and x < vision.board_edges[1][0] and y > vision.board_edges[0][1] and y < vision.board_edges[1][1]: # Check if the circle is in the board.
                            cv2.circle(img, center, radius=1, color=(0, 255, 0), thickness=-1)
                            cv2.circle(img, center, radius, (0, 255, 0), 2)
                            if morph[center[1], center[0]] == 0:                                                                # Check if the center is black
                                vision.found_black.append([x, y, radius, color, False])
                                text = "b" + vision.color_map[color]
                                cv2.putText(img, text, (center[0] + 20, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
                            elif morph[center[1], center[0]] == 255:                                                            # Check if the center is white
                                vision.found_white.append([x, y, radius, color, False])
                                text = "w" + vision.color_map[color]
                                cv2.putText(img, text, (center[0] + 20, center[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))                        

        # Make sure there are only a certain number of pieces on the board.
        num_pieces = {
            "p": [0,8],
            "r": [0,2],
            "n": [0,2],
            "b": [0,2],
            "q": [0,3],
            "k": [0,1]
        }
        # Test each shape found to determine if its in a square.
        # ((x2 - x1)**2 + (y2 - y1)**2)**0.5 <= r1 + r2    <- Determines if two circles intersect or are inside each other.
        for shape in vision.found_black:
            if shape[4] == False:
                for i, row in enumerate(vision.board_positions):
                    for j, square in enumerate(row):
                        if (((shape[0] - square[0])**2 + (shape[1] - square[1])**2)**0.5 <= shape[2] + vision.radius) and vision.board[i][j] == "-":
                            shape[4] = True
                            # Shape is in point, add it to the board position.
                            # Make sure there are only a certain number of pieces on the board.
                            piece = vision.color_map[shape[3]]
                            num_pieces[piece][0] += 1
                            if num_pieces[piece][0] <= num_pieces[piece][1]:
                                out = "b" + piece + str(num_pieces[piece][0])
                                #print(out)
                                vision.board[i][j] = out     # Add the black piece to the board.
                                break
                                #print(vision.board)
        #cv2.putText(img, str(num_pieces), (7, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        #cv2.putText(img, str(len(vision.found_black)), (7, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0))
        # Reset values.
        num_pieces = {
            "p": [0,8],
            "r": [0,2],
            "n": [0,2],
            "b": [0,2],
            "q": [0,3],
            "k": [0,1]
        }
        for shape in vision.found_white:
            if shape[4] == False:
                for i, row in enumerate(vision.board_positions):
                    for j, square in enumerate(row):
                        if (((shape[0] - square[0])**2 + (shape[1] - square[1])**2)**0.5 <= shape[2] + vision.radius) and vision.board[i][j] == "-":
                            shape[4] = True
                            # Shape is in point, add it to the board position.
                            # Make sure there are only a certain number of pieces on the board.
                            piece = vision.color_map[shape[3]]
                            num_pieces[piece][0] += 1
                            if num_pieces[piece][0] <= num_pieces[piece][1]:
                                out = "w" + piece + str(num_pieces[piece][0])
                                vision.board[i][j] = out    # Add the white piece to the board.
                                break
                                #print(vision.board)


        #cv2.imshow("blurred",blurred)
        #cv2.imshow("edges", edges)
        if vision.show_image == True:
            mask = vision.color_masks["green"]
            cv2.imshow("mask", mask)
            kernel = np.ones((5,5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
            cv2.imshow("morph", mask)
            edges = cv2.Canny(mask, 10, 200, apertureSize=3) 
            cv2.imshow("edges", edges)
            # Draw the points onto the image.
            for i, row in enumerate(vision.board_positions):
                for k, j in enumerate(row):
                    cv2.circle(img, (int(j[0]),int(j[1])), radius=vision.radius, color=(0, 0, 255), thickness=1)
                    #cv2.putText(img, vision.board[i][k], (int(j[0]) - 3,int(j[1])), cv2.FONT_HERSHEY_SIMPLEX, 0.25, (0, 0, 255))
                    pass
            cv2.imshow("CV", img)
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        #pil_img = Image.fromarray(img)
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