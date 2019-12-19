import cv2
import numpy as np


class FaceFinder(object):
    def __init__(self):
        pass
        #self.face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
        #self.face_cascade.load('')
        #self.faces = None

    def getFace(self, _frame):
        pass
        #self.faces = self.face_cascade.detectMultiScale(_frame, 1.03, 5)

        #return np.array(self.faces)

"""
print(faces.shape)
print("Number of faces detected: " + str(faces.shape[0]))

for (x,y,w,h) in faces:

    cv2.rectangle(ourFace,(x,y),(x+w,y+h),(255, 200, 10),10)

plt.figure(figsize=(12,12))
plt.imshow(ourFace, cmap='gray')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()
"""
