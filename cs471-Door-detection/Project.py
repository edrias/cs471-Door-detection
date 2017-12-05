import numpy as np


import matplotlib.pyplot as plt
import cv2
import math
class door_detection:


    def __init__(self,img_door):
        self.img_door = img_door
        self.test_door = img_door
        self.gray_door = cv2.cvtColor(img_door, cv2.COLOR_BGR2GRAY)
        self.height, self.width, self.channels = self.img_door.shape

        self.upper_half = self.height/2
        self.lower_half = self.height

        if self.height > 1024 and self.width > 768:
            # if self.height > self.width:
            self.img_door = cv2.resize(self.img_door, (1024, 768))
            self.gray_door = cv2.cvtColor(self.img_door, cv2.COLOR_BGR2GRAY)
            self.height, self.width, self.channels = self.img_door.shape

    def draw_corners(self):
        for line in self.line_coords:
            #point one of line
            x1 = line[0][0]
            y1 = line[0][1]
            #point 2 of line
            x2 = line[1][0]
            y2 = line[1][1]
            print(line)
            cv2.circle(self.img_door, (x1, y1), 1, 255, 3)
            cv2.circle(self.img_door, (x2, y2), 1, 255, 3)
        return self.img_door

    def draw(self):
        for square in self.square_coords:

            #print square
            x1 = square[0][0]
            y1 = square[0][1]
            x2 = square[1][0]
            y2 = square[1][1]
            x3 = square[2][0]
            y3 = square[2][1]
            x4 = square[3][0]
            y4 = square[3][1]
            #draw corners
            cv2.circle(self.img_door, (x1, y1), 1, 255, 3)
            cv2.circle(self.img_door, (x2, y2), 1, 255, 3)
            cv2.circle(self.img_door, (x3, y3), 1, 255, 3)
            cv2.circle(self.img_door, (x4, y4), 1, 255, 3)

            #draw lines
            cv2.line(self.img_door, (x1, y1), (x2, y2), (1, 0, 255), 3)
            cv2.line(self.img_door, (x2, y2), (x3, y3), (1, 255, 1), 3)
            cv2.line(self.img_door, (x3, y3), (x4, y4), (1, 0, 255), 3)
            cv2.line(self.img_door, (x4, y4), (x1, y1), (1, 255, 1), 3)

            #draw rectangle
            pts = np.array([[x1,y1],[x2,y2], [x3, y3], [x4,y4] ] )
            cv2.fillPoly(self.img_door, pts = [pts], color =  (255,0,0))

        return self.img_door

    def Corner_Detection(self):
        self.corners_loc = []
        self.gray_door = np.float32(self.gray_door)
        self.corners = cv2.goodFeaturesToTrack(self.gray_door, 500, 0.04, 10)
        self.corners = np.int0(self.corners)
        for corner in self.corners:
            x, y = corner.ravel()
            #cv2.circle(self.img_door, (x, y), 1, 255, 3)
            self.corners_loc.append([x,y])

        return self.img_door

    def find_lines(self):
        print (self.height, self.width)
        self.line_coords = []#line coordinates
        self.taken = [] #corners that have been used once already.


        if self.width >  self.height: #draw vertical lines
            self.line_direction = 'V'#vertical lines
            for corner in self.corners:#loop through corner coordinates
                x1, y1 = corner.ravel()
                if y1 < self.height/2:#take corners that are above midpoint of image, don't wanna more lines than needed
                    for next_corner in self.corners:
                        x2, y2 = next_corner.ravel()
                        #check if corner coordinate is close to same y plane
                        if abs(x2 - x1) < 3 and [x1,y1] not in self.taken and [x2,y2] not in self.taken:
                            if abs(y2 - y1) > self.height /2: #don't draw short lines. Door i usually longest feature.
                                if y1 < self.height/2:# classify where the coordinate is relative to the image.
                                    self.line_coords.append(((x1,y1,'upper'),(x2,y2,'lower')))
                                else:
                                   self.line_coords.append(((x1,y1,'lower'),(x2,y2,'upper')))
                                #coordinates have been used once, don't use them again.
                                self.taken.append([x1,y1])
                                self.taken.append([x2,y2])

        else:
            self.line_direction = 'H'
            #draw horizontal lines
            for corner in self.corners:#loop through corner coordinates
                x1, y1 = corner.ravel()
                if x1 < self.width/2:#take corners that are above midpoint of image, don't wanna more lines than needed
                    for next_corner in self.corners:
                        x2, y2 = next_corner.ravel()
                        #check if corner coordinate is close to same y plane

                        if abs(y2 - y1) < 5 and [x1,y1] not in self.taken and [x2,y2] not in self.taken:
                            if abs(x2 - x1) > self.width*.2 and abs(x2- x1) < self.width*.8 \
                                    and x1 < self.width*.8 and x1 > self.width*.2\
                                    and y1 > self.height*.1:
                                if x1 < self.width/2:# classify where the coordinate is relative to the image.
                                    self.line_coords.append([[x1,y1,'left'],[x2,y2,'right']])
                                else:
                                   self.line_coords.append(([[x1,y1,'right'],[x2,y2,'left']]))
                                #coordinates have been used once, don't use them again.
                                self.taken.append([x1,y1])
                                self.taken.append([x2,y2])

        return self.img_door

    def draw_opposite_line(self):
        taken = []
        self.square_coords = []
        if self.line_direction == 'V':
            self.line_coords = self.sort_x()
            print(self.line_coords)
            for corners in self.line_coords:
                x1 = corners[0][0]
                y1 = corners[0][1]
                x2 = corners[1][0]
                y2 = corners[1][1]
                for next_corner in self.line_coords:
                        X1 = next_corner[0][0]
                        Y1 = next_corner[0][1]
                        X2 = next_corner[1][0]
                        Y2 = next_corner[1][1]
                        if [x1,y1,x2,y2] != [X1,Y1,X2,Y2]:
                            #don't draw horizontal lines that are too close to each other
                            if abs(y1- Y1) <20 and [x1,y1] not in taken and [X1, Y1] not in taken:
                                self.square_coords.append(((x1, y1), (X1, Y1), (X2, Y2), (x2, y2)))
                                taken.append([x1,y1])
                                taken.append([X1,Y1])

        else:
            for corners in self.line_coords:
                x1 = corners[0][0]
                y1 = corners[0][1]
                x2 = corners[1][0]
                y2 = corners[1][1]
                for next_corner in self.line_coords:
                    X1 = next_corner[0][0]
                    Y1 = next_corner[0][1]
                    X2 = next_corner[1][0]
                    Y2 = next_corner[1][1]
                    if [x1, y1, x2, y2] != [X1, Y1, X2, Y2]:#don't use same point!
                        # don't draw horizontal lines that are too close to each other.
                        if abs(x1 - X1) < 10 and [x1, y1] not in taken and [X1,Y1] not in taken and abs(y1 - Y1) > self.height/2:
                            self.square_coords.append(((x1,y2),(x2,y2),(X2,Y2), (X1,Y1)))
                            taken.append([x1, y1])
                            taken.append([X1, Y1])

        return self.img_door

    def get_top__angle(self, x1,y1,x2,y2):
        [x,y] = [x1-x2,y1-y2]
        if x == 0:
            return 90
        else:
            rad = math.atan(y/x)
            angle = rad*(180/math.pi)

        top_angle = angle + 90

        return top_angle

    def verify_point(self, top_angle,x1,y1,x2,y2):
        angle = self.get_top__angle(x1,y1,x2,y2)
        if angle < top_angle + 1 and angle > top_angle -1:
            return True
        else:
            return False

    def sort_x(self):
        print self.line_coords[0][0][0]

        return sorted(self.line_coords, key = lambda x: x[0][0])
        #return sorted (self.line_coords[0][0])

img_door = cv2.imread('room.jpeg')
dt = door_detection(img_door)

img_door = dt.Corner_Detection()

#cv2.imshow('image', img_door)

line_door = dt.find_lines()

cv2.imshow('lines',img_door)
#line_door = dt.draw_opposite_line()

opposite_lines = dt.draw_opposite_line()

cv2.imshow('opposite',opposite_lines)


#corner_door = dt.draw_corners()
door = dt.draw()
cv2.imshow('corner door', door)

cv2.waitKey(0)
#cv2.imshow('harris1',img_door)