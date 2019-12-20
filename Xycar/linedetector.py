# -*- coding: utf-8 -*-

import time
import rospy
import cv2
import numpy as np
import math
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

class LineDetector:
    def __init__(self, topic, ros_node=True):
        self.ros_node = ros_node
        
        self.scan_height = 100
        self.scan_width = 200

        self.image_width = 640
        self.image_height = 480

        self.roi_vertical_pos = 310 #230

        self.mask = np.zeros(shape=(self.scan_height, self.image_width), dtype=np.uint8)       #이진화된 이미지
        self.edge = np.zeros(shape=(self.scan_height, self.image_width), dtype=np.uint8)       #외곽
        self.edge_bird_view = np.zeros(shape=(self.scan_height, self.image_width), dtype=np.uint8)       #외곽
        self.edge_and = np.zeros(shape=(self.scan_height, self.image_width), dtype=np.uint8)
        self.cam_view = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.bird_view = np.zeros(shape=(480, 640, 3), dtype=np.uint8) #bird view
        self.bird_view_record = np.zeros(shape=(480, 640, 3), dtype=np.uint8) #bird view

        w = self.image_width
        h = self.image_height        

        self.src = np.float32([[w * 0.9, h], [w * 0.1, h], [w * 0.1, h * 0.5], [w * 0.9, h * 0.5]])
        self.dst = np.float32([[w * 0.65, h], [w * 0.35, h], [w * (-0.5), 0], [w * 1.5, 0]])
        
        self.v_threshold = 0
        
        self.hsv = [0, 0, 100, 255, 25, 255]
        
        self.angle_avr= 0
        
        self.bridge = CvBridge()
        rospy.Subscriber(topic, Image, self.conv_image)
        
        if self.ros_node:
            self.recorder = cv2.VideoWriter(
                '/home/nvidia/xycar/src/eureka/record_100.avi',
                cv2.VideoWriter_fourcc(*'MJPG'),
                30,
                (640, 480)
            )
                
    def __del__(self):
        if self.ros_node:
            self.recorder.release()
        cv2.destroyAllWindows()
        
    def conv_image(self, data):
        self.cam_view = self.bridge.imgmsg_to_cv2(data, 'bgr8')
        self.make_bird_view()
        self.make_mask()
        self.make_edge()
        self.show_images()
        self.record()

    def show_images(self):
        #self.mask = cv2.resize(self.mask, (440,330))
        #cv2.imshow("mask", self.mask)
        #self.edge = cv2.resize(self.edge, (440,330))
        #cv2.imshow("edge", self.edge)
        #self.edge_bird_view = cv2.resize(self.edge_bird_view, (440,330))
        #cv2.imshow("edge_bird_view", self.edge_bird_view)
        #self.bird_view = cv2.resize(self.bird_view, (440,330))
        #cv2.imshow("bird_view", self.bird_view)
        #self.edge_and = cv2.resize(self.edge_and, (440,330))
        #cv2.imshow("edge_and", self.edge_and)
        
        cv2.waitKey(1)
        
    def make_view_to_bird_view(self, _view_src, view_res):
        mat = cv2.getPerspectiveTransform(self.src, self.dst)
        mat_dst = cv2.getPerspectiveTransform(self.dst, self.src)
        
        view_res = cv2.warpPerspective(_view_src, mat, (self.image_width, self.image_height))
        return view_res
        
    def make_bird_view(self):
        mat = cv2.getPerspectiveTransform(self.src, self.dst)
        mat_dst = cv2.getPerspectiveTransform(self.dst, self.src)
    
        self.bird_view = cv2.warpPerspective(self.cam_view, mat, (self.image_width, self.image_height))
        self.bird_view_record = cv2.warpPerspective(self.cam_view, mat, (self.image_width, self.image_height))
    
    def make_mask(self):
        hsv = cv2.cvtColor(self.cam_view, cv2.COLOR_BGR2HSV)

        avg_value = np.average(hsv[:, :, 2])
        self.v_threshold = avg_value * 0.01

        lbound = np.array([self.hsv[0], self.hsv[1], self.hsv[2] + self.v_threshold], dtype=np.uint8)
        ubound = np.array([self.hsv[3], self.hsv[4], self.hsv[5]], dtype=np.uint8)

        self.mask = cv2.inRange(hsv, lbound, ubound)
    
    def make_edge(self):
        self.edge = cv2.equalizeHist(self.mask)
        blur = cv2.GaussianBlur(self.cam_view, (3, 3), 0)
        self.edge = cv2.Canny(blur, 60, 120)
        
        #cv2.bitwise_and(self.edge, self.mask, self.edge_and)
        cv2.bitwise_and(self.edge, self.mask, self.edge)
        self.edge_bird_view = self.make_view_to_bird_view(self.edge, self.edge_bird_view)
                
        roi_x_start = 40
        roi_x_end = 600

        roi_line = self.edge_bird_view[self.roi_vertical_pos:self.roi_vertical_pos + self.scan_height, 40:600]
        
        linesP = cv2.HoughLinesP(roi_line, 10, np.pi / 180, 50, None, 50, 10)
        angle_list = []
        angle_cnt = 0

        if linesP is not None:
            for i in range(0, len(linesP)):
                l = linesP[i][0]

                if l[3] > l[1]:
                    l[0], l[1], l[2], l[3] = l[2], l[3], l[0], l[1]

            sorted(linesP, key=lambda x: x[0][0])
                
            for i in range(0, len(linesP), 1 if len(linesP) == 1 else len(linesP) - 1):
                angle = math.atan2(l[1] - l[3], l[0] - l[2]) * 180 / math.pi - 90
                
                if angle > 80 or angle < -80:
                    continue
                if (angle <= 10 and angle >= -4) and l[0] > 240:
                    angle = 12
                    
                #if ((l[0] > 10 and l[0] < 60) or (l[0] < 470 and l[0] > 420)):
                angle_cnt += 1
                angle_list.append(angle)

                cv2.line(self.bird_view, (l[0] + roi_x_start, l[1] + self.roi_vertical_pos), (l[2] + roi_x_start, l[3] + self.roi_vertical_pos), (0, 0, 255), 3, cv2.LINE_AA)
            if angle_cnt >= 1:
                self.angle_avr = sum(angle_list) / angle_cnt
            else:
                self.angle_avr = -99
        else:
            pass
            #print('no line')
        
    def detect_angle(self):
        return self.angle_avr
    
    def record(self):
        if self.ros_node:
            self.recorder.write(self.cam_view)
        
