import time
import cv2
from linedetector import LineDetector

cap = cv2.VideoCapture('2.avi')
detector = LineDetector('', ros_node=False)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) & 0xff == 27:
        break

    detector.conv_image(frame)
    l, r = detector.detect_lines()
    detector.show_images(l, r)
    time.sleep(0.03)
    
cap.release()
cv2.destroyAllWindows()
