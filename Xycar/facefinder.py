import cv2
import numpy as np


class FaceFinder(object):
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('/home/nvidia/xycar/src/eureka/src/haarcascade_frontalface_default.xml')
        self.faces = None

    def getFace(self, _frame):
        self.faces = self.face_cascade.detectMultiScale(_frame, 1.03, 5)

        return np.array(self.faces)
