import cv2
from matplotlib import pyplot as plt

ourFace = cv2.imread("../image/recognizeTest.png")

face_cascade = cv2.CascadeClassifier(
    '../haarcascades/haarcascade_frontalface_default.xml'
)

faces = face_cascade.detectMultiScale(ourFace, 1.03, 5)

print(type(faces))
print(faces.shape)
print("Number of faces detected: " + str(faces.shape[0]))

for (x,y,w,h) in faces:

    cv2.rectangle(ourFace,(x,y),(x+w,y+h),(255, 200, 10),10)

plt.figure(figsize=(12,12))
plt.imshow(ourFace, cmap='gray')
plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
plt.show()