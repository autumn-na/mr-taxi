try:
    import urllib2  # python2
except:
    import urllib.request
import json
import time
from Tests.facefinder import *

URL_ROOT = 'http://10.42.0.165:8080'
LOCAL_URL_ROOT = 'http://127.0.0.1:8080'


class TaxiDriver(object):
    def __init__(self):
        self.cost = 0
        self.is_guest_in = False
        self.pickup_time = 0
        self.drive = True  # check can drive
        self.face_finder = FaceFinder()
        pass

    def find(self):
        #urllib.request.urlopen(URL_ROOT + '/find')
        self.is_guest_in = False
        urllib2.urlopen(URL_ROOT + '/find')

    def pickUp(self, _dest):
        #urllib.request.urlopen(URL_ROOT + '/pickup?dest=' + _dest)
        self.is_guest_in = True
        urllib2.urlopen(URL_ROOT + '/pickup?dest=' + _dest)

    def arrive(self):
        #urllib.request.urlopen(URL_ROOT + '/arrive?cost=' + str(self.cost))
        self.is_guest_in = True
        urllib2.urlopen(URL_ROOT + '/arrive?cost=' + str(self.cost))

    def getData(self):
        #response = urllib.request.urlopen(URL_ROOT + '/getdata')
        response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data

    def getDest(self):
        #response = urllib.request.urlopen(URL_ROOT + '/getdata')
        response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data['dest']

    def getIsArrived(self):
        # response = urllib.request.urlopen(URL_ROOT + '/getdata')
        response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data['is_arrived']

    def procFind(self, _frame):
        if self.getData()['is_found'] == False and self.face_finder.getFace(_frame).shape[0] == 1 and self.is_guest_in == False:
            self.drive = False
            self.find()
            print('Find!')

    def procPickup(self):
        if self.getData()['is_found'] == True and self.getData()['is_picked_up'] == False and self.getData()['dest'] != '':
            self.drive = True
            self.pickup_time = time.time()
            self.pickUp(self.getData()['dest'])
            print('Pickup! Dest: ' + self.getData()['dest'])

    def procDrive(self):
        if self.getData()['is_found'] == True and self.getData()['is_picked_up'] == True and self.getData()['dest'] != '' and \
                self.getData()['is_arrived'] == False:
            self.drive = True
            print('now driving...')

    def procArrive(self):
        if self.getData()['is_found'] == True and self.getData()['is_picked_up'] == True and self.getData()['dest'] != '' and \
                self.getData()['is_arrived'] == False and time.time() - self.pickup_time >= 5:
            self.drive = False
            self.arrive()
            print('Arrived!')

    def procPay(self):
        if self.is_guest_in == True and self.getData()['dest'] == '':
            self.is_guest_in = False
            self.drive = False
            print('Paid!')
