# wa submission

## answer (photo)
![solution_img](https://github.com/user-attachments/assets/d9adcf17-822d-48a6-9443-88e6a16b831f)

## methodology
### loading and processing the image
i first loadeed the image, and converted it to the hsv color space. this is because its much easier to work with the color red if we use an hsv color space. i then made a mask that highlights only the red part of the image by setting a color range for red.

### find contours
i then used opencv's contour detection to find the shapes/outlines that represented the red cones. 

### dividing the image in half
i found the middle of the image by dividing the image's width in half. that way i was able to separate the cones into two groups: cones whose centers are on the left side of the image; cones whose centers are on the right side of the image

### calculate the centers
for each contour found (where each contour represents a cone), i calculated its center. i did this by using the moments of the contour, which gave the average position (as an (x,y) pair) of the shape.

### fitting lines through the cones (and drawing them)
once i found the centers of the contours, i fit a line through the left side cones, and then another line through the right side cones. once that was done, i drew the two lines onto the image.

## what i tried & why it didn't work
### finding the correct color range
one of the main challenges i dealt with, specifically at the beginning, was defining the correct hsv color range to accurately be able to isolate only the cones. for example, if the color range was too narrow, then not enough of the cones would be detected. if the color range was too wide, then the door on the left side of the image, and even the emergency exit signs would be detected.

### learning opencv
i was pretty new to opencv, so i spent quite a lot of time googling about the various functions (i.e. contour detection, moment calculation, line fitting) to understand how/why they worked. some of my initial attempts did not yield the results i expected. for example, when i was first using the contours, it had deteced some crazy, not-a-cone things.

### learning numpy
i also haven't had a ton of experience with numpy either. so, i also spent time understanding how numpy handled arrays (something that made fitting lines using opencv much easier). lots of trial and error!

## what libraries were used
- opencv ('cv2' in the solution.py file)
  - used it for image processing, contour detection, and fitting/drawing lines through the cones
- numpy
  - used it for hadnling arrays and working with the coordinates of the contours and their centers
