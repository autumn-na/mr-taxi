from imuread import ImuRead
import datetime


class pay(object):
    def __init__(self):
        self.imu = ImuRead('/diagnostics')

    def distancecalculator(self, imudistance):
        r, p, y = self.imu.get_data()
        distance = y
        pay = 3000
        a = distance // 1
        pay += a * 100
