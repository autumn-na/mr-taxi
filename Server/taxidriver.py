import urllib.request  # remove urllib in xycar
#import urllib2
import random
import json

URL_ROOT = 'http://10.42.0.165:8080'
LOCAL_URL_ROOT = 'http://127.0.0.1:8080'


class TaxiDriver(object):
    def __init__(self):
        self.cost = 0
        self.is_guest_in = False
        pass

    def find(self):
        urllib.request.urlopen(LOCAL_URL_ROOT + '/find')
        self.is_guest_in = False
        # urllib2.urlopen(URL_ROOT + '/pickup?dest=' + _dest)

    def pickUp(self, _dest):
        urllib.request.urlopen(LOCAL_URL_ROOT + '/pickup?dest=' + _dest)
        self.is_guest_in = True
        #urllib2.urlopen(URL_ROOT + '/pickup?dest=' + _dest)

    def arrive(self):
        urllib.request.urlopen(LOCAL_URL_ROOT + '/arrive?cost=' + str(self.cost))
        self.is_guest_in = True
        #urllib2.urlopen(URL_ROOT + '/arrive')

    def getData(self):
        response = urllib.request.urlopen(LOCAL_URL_ROOT + '/getdata')
        # response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data

    def getDest(self):
        response = urllib.request.urlopen(LOCAL_URL_ROOT + '/getdata')
        #response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data['dest']

    def getIsArrived(self):
        response = urllib.request.urlopen(LOCAL_URL_ROOT + '/getdata')
        #response = urllib2.urlopen(URL_ROOT + '/getdata')
        data = json.load(response)
        return data['is_arrived']
