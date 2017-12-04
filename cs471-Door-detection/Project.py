import numpy as np
import matplotlib.pyplot as plt
import cv2

class door_detection:


    def __init__(self,img_door):
        self.img_door = img_door
        self.test_door = img_door
        self.gray_door = cv2.cvtColor(img_door, cv2.COLOR_BGR2GRAY)
        self.height, self.width, self.channels = self.img_door.shape

        self.upper_half = self.height/2
        self.lower_half = self.height

    def Corner_Detection(self):
        self.corners_loc = []
        self.gray_door = np.float32(self.gray_door)
        self.corners = cv2.goodFeaturesToTrack(self.gray_door, 250, 0.04, 10)
        self.corners = np.int0(self.corners)
        print self.corners.shape
        #print self.corners
        #print self.corners_loc[:50]
        for corner in self.corners:
            x, y = corner.ravel()
            cv2.circle(self.img_door, (x, y), 1, 255, 3)
            self.corners_loc.append([x,y])

        return self.img_door

    def draw_lines(self):
        print (self.height, self.width)
        self.line_coords = []
        self.line_corners = []
        #Draw vertical lines
        if self.width >  self.height:
            self.line_direction = 'V'#vertical lines
            for corner in self.corners:
                x1, y1 = corner.ravel()
                if y1 < self.height/2:
                    for next_corner in self.corners:
                        x2, y2 = next_corner.ravel()
                        if abs(x2 - x1) < 10:  # if dot is horizontal within 10 pixels
                            # print y2,y1
                            # print x2,x1
                            if abs(y2 - y1) > self.height /2: #and abs(y2 - y1) < self.height/2:
                                cv2.line(self.img_door, (x1, y1), (x2, y2), (1, 0, 255), 1)
                                if y1 < self.height/2:
                                    self.line_coords.append([[x1,y1,'upper'],[x2,y2,'lower']])
                                else:
                                   self.line_coords.append(([[x1,y1,'lower'],[x2,y2,'upper']]))
                                self.line_corners.append([x1,y1,False])
                                self.line_corners.append([x2,y2,False])
        else:
            self.line_direction = 'H'
            #draw horizontal lines
            for corner in self.corners:
                x1, y1 = corner.ravel()
                for next_corner in self.corners:
                    x2, y2 = next_corner.ravel()
                    if abs(y2 - y1) < 15:  # if dot is vertical within 10 pixels
                        # print y2,y1
                        # print x2,x1
                        if abs(x2 - x1) < self.width - (self.width*.4) and abs(x2-x1) > (self.width/4):
                            cv2.line(self.img_door, (x1,y1), (x2,y2), (1, 0, 255),1)
                            self.line_coords.append([x1, y1, x2, y2])
                            self.line_corners.append([x1, y1, False])
                            self.line_corners.append([x2, y2, False])

        return self.img_door

    def draw_opposite_line(self):
        for i in self.line_coords:
            print i
        for corner in self.line_corners:
            x1, y1,bool1 = corner
            for next_corner in self.line_corners:
                x2, y2,bool2 = next_corner
                if abs(y2 - y1) < 30:  # if dot is vertical within 10 pixels
                    # print y2,y1
                    # print x2,x1
                    if abs(x2 - x1) < self.width/2:# - (self.width * .4) and abs(x2 - x1) > (self.width / 4):
                        cv2.line(self.img_door, (x1, y1), (x2, y2), (1, 0, 255), 1)

        return self.img_door
img_door = cv2.imread('room.jpeg')

dt = door_detection(img_door)

img_door = dt.Corner_Detection()

cv2.imshow('image', img_door)

line_door = dt.draw_lines()

cv2.imshow('lines',img_door)
line_door = dt.draw_opposite_line()

cv2.imshow('opposite lines', line_door)
cv2.waitKey(0)
#cv2.imshow('harris1',img_door)