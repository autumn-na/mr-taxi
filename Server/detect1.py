#!/usr/bin/env python

# -*- coding: utf-8 -*-


import time

from facefinder import *
from taxidriver import *

cap = cv2.VideoCapture('2.avi')


class Taxi:
    def __init__(self):
        self.frame = []

        self.scan_height = 100
        self.scan_width = 200

        self.image_width = 640
        self.image_height = 480

        self.roi_vertical_pos = 230  # 230

        self.taxi_driver = TaxiDriver()
        self.face_finder = FaceFinder()

        self.start_time = time.time()
        self.cur_time = 0


    def show_images(self):
        cv2.imshow("cam_view", self.frame)

    def procTime(self):
        self.cur_time = time.time() - self.start_time

    def procFind(self):
        if self.taxi_driver.getData()['is_found'] == False and self.face_finder.getFace(self.frame).shape[0] == 1 and  self.taxi_driver.is_guest_in == False:
            self.taxi_driver.find()
            print('Find!')

    def procPickup(self):
        if self.taxi_driver.getData()['is_found'] == True and self.taxi_driver.getData()['is_picked_up'] == False and self.taxi_driver.getData()['dest'] != '':
            self.taxidriver.pickUp(self.taxidriver.getData()['dest'])
            print('Pickup! Dest: ' + self.taxidriver.getData()['dest'])

    def procDrive(self):
        if  self.taxi_driver.getData()['is_found'] == True and self.taxi_driver.getData()['is_picked_up'] == True and self.taxidriver.getData()['dest'] != '' and \
                self.taxi_driver.getData()['is_arrived'] == False:
            print('now driving...')

    def procArrive(self):
        if self.taxi_driver.getData()['is_found'] == True and self.taxi_driver.getData()['is_picked_up'] == True and self.taxidriver.getData()['dest'] != '' and \
                self.taxi_driver.getData()['is_arrived'] == False:

            self.taxidriver.arrive()
            print('Arrived!')

    def procPay(self):
        if self.taxi_driver.is_guest_in == True and self.taxi_driver.getData()['dest'] == '':
            self.taxi_driver.is_guest_in = False

            print('Paid!')


taxi = Taxi()
while True:
    ret, taxi.frame = cap.read()
    if not ret:
        break
    if cv2.waitKey(1) & 0xFF == 27:
        break

    taxi.show_images()

    taxi.procTime()

    taxi.procFind()
    taxi.procPickup()
    taxi.procDrive()
    taxi.procArrive()
    taxi.procPay()

    time.sleep(0.001)

cap.release()
cv2.destroyAllWindows()
