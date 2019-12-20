#!/usr/bin/env python

# -*- coding: utf-8 -*-


from Tests.taxidriver import *
from Tests.qrreader import *

reader = QRReader()
print(reader.getQRText(cv2.imread('qr.png')))

cap = cv2.VideoCapture('2.avi')

class Taxi:
    def __init__(self):
        self.frame = []
        self.last_time = 0
        self.scan_height = 100
        self.scan_width = 200

        self.image_width = 640
        self.image_height = 480

        self.roi_vertical_pos = 230  # 230

        self.taxi_driver = TaxiDriver()

    def show_images(self):
        cv2.imshow("cam_view", self.frame)


taxi = Taxi()
taxi.last_time = time.time()
while True:
    ret, taxi.frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

    #taxi.show_images()
    print(time.time() - taxi.last_time)

    #taxi.taxi_driver.procFind(taxi.frame)
    #taxi.taxi_driver.procPickup()
    #taxi.taxi_driver.procDrive()
    #taxi.taxi_driver.procArrive()
    #taxi.taxi_driver.procPay()
    #print(taxi.taxi_driver.face_finder.getFace(taxi.frame))

    time.sleep(0.001)
cap.release()
cv2.destroyAllWindows()
