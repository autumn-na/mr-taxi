# -*- coding: utf-8 -*-

import time
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

IMAGE_H = 480
IMAGE_W = 640

class BirdView:
    def __init__(self, topic):
        self.bird_view = np.zeros(shape=(480, 640, 3), dtype=np.uint8)
        self.bridge = CvBridge()
        
        self.src = np.float32([[0, IMAGE_H], [640, IMAGE_H], [0, 0], [IMAGE_W, 0]])
        self.dst = np.float32([[640, IMAGE_H], [640, IMAGE_H], [0, 0], [IMAGE_W, 0]])
        
        rospy.Subscriber(topic, Image, self.view)
        
    def view(self, data):
        self.bird_view = self.bridge.imgmsg_to_cv2(data, 'bgr8')
    
        mat = cv2.getPerspectiveTransform(self.src, self.dst)
        mat_dst = cv2.getPerspectiveTransform(self.dst, self.src)
    
        self.bird_view = cv2.warpPerspective(self.bird_view, mat, (IMAGE_W, IMAGE_H))
        
        cv2.imshow("bird_view", self.bird_view)
        cv2.waitKey(1)
      
        
