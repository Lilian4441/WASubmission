import cv2
import numpy as np

# load the image
img = cv2.imread('image.png')

# make sure the image actually loaded, otherwise throw an error
if img is None:
    print("Error: Could not load the image.")
else:
    # convert the image to hsv to make it easier to work with colors like red
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # set the color range for red (b/c red is the range we're looking for)
    lower_red = np.array([0, 165, 165])
    upper_red = np.array([10, 225, 225])

    # create a mask so that only the red parts of the image are white, and everything else is black
    mask = cv2.inRange(hsv, lower_red, upper_red)

    # find all the shapes (contours) in the mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # figure out the middle of the image so we can divide teh cones into left and right
    image_height, image_width, _ = img.shape
    middle_x = image_width // 2  # the x-coordinate that splits the image in half

    # two lists to store centroids of the left and right side contours
    left_centroids = []
    right_centroids = []

    # loop through each contour to find the center of each shape
    for contour in contours:
        # find the center of each contour (a fancy way of getting the center)
        M = cv2.moments(contour)

        # make sure the contour has an actual area (avoiding division by zero)
        if M["m00"] != 0:
            # calculate the x and y coordinates of the center
            contour_X = int(M["m10"] / M["m00"])  # the x center
            contour_Y = int(M["m01"] / M["m00"])  # the y center

            # if the center is on the left side of the image, add it to the left list
            if contour_X < middle_x:
                left_centroids.append((contour_X, contour_Y))
            # otherwise, it's on the right side
            else:
                right_centroids.append((contour_X, contour_Y))

    # fit a line through the centroids on the left side
    if len(left_centroids) > 1:  # need at least two points to draw a line
        left_centroids = np.array(left_centroids, dtype=np.float32)  # make it an array
        [vx1, vy1, x1, y1] = cv2.fitLine(left_centroids, cv2.DIST_L2, 0, 0.01, 0.01)

        # convert the values to simple numbers, just to avoid any issues
        vx1 = vx1.item()
        vy1 = vy1.item()
        x1 = x1.item()
        y1 = y1.item()

        # figure out where the line starts and ends for the left side
        left_y1 = int((-x1 * vy1 / vx1) + y1)
        left_y2 = int(((image_width - x1) * vy1 / vx1) + y1)

        # draw the line on the left side
        cv2.line(img, (0, left_y1), (image_width, left_y2), (255, 0, 0), 2)

    # same thing but now for the right side
    if len(right_centroids) > 1:
        right_centroids = np.array(right_centroids, dtype=np.float32)
        [vx2, vy2, x2, y2] = cv2.fitLine(right_centroids, cv2.DIST_L2, 0, 0.01, 0.01)

        # convert the values to simple numbers for the right side too
        vx2 = vx2.item()
        vy2 = vy2.item()
        x2 = x2.item()
        y2 = y2.item()

        # figure out where the line starts and ends for the right side
        right_y1 = int((-x2 * vy2 / vx2) + y2)
        right_y2 = int(((image_width - x2) * vy2 / vx2) + y2)

        # draw the line on the right side
        cv2.line(img, (0, right_y1), (image_width, right_y2), (255, 0, 0), 2)

    # show the final image with both red lines
    cv2.imshow("Fitted Lines Through Contours", img)
    cv2.waitKey(0)  # wait for a key press to close the window
    cv2.destroyAllWindows()  # close everything once we're done
