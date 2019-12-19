from taxidriver import *
import time


class TaxiTest(object):
    def __init__(self):
        self.taxidriver = TaxiDriver()
        self.find()

    def find(self):
        #if xycar find person
        input('Input Enter to start test')
        time.sleep(3)
        print('find')
        self.taxidriver.find()
        self.stop()

    def stop(self):
        #xycar stops

        print('stop')
        self.pickup()

    def pickup(self):
        while self.taxidriver.getData()['dest'] == '':
            pass
        print('pickup! Dest: ' + self.taxidriver.getData()['dest'])
        self.taxidriver.pickUp(self.taxidriver.getData()['dest'])
        self.drive()

    def drive(self):
        #xycar drives track
        print('now driving...')
        time.sleep(3)
        self.arrive()

    def arrive(self):
        #xycar stops

        print('arrive!')
        self.taxidriver.arrive()
        self.pay()

    def pay(self):
        #xycar drives track

        while self.taxidriver.getData()['dest'] != '':
            pass

        print('finished!')
        self.find()

taxitest = TaxiTest()



