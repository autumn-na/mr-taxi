import pyzbar.pyzbar as pyzbar
import cv2

class QRReader(object):
    def __init__(self):
        pass

    def getQRText(self, _frame):
        gray = cv2.cvtColor(_frame, cv2.COLOR_BGR2GRAY)

        decoded = pyzbar.decode(gray)

        for d in decoded:
            barcode_data = d.data.decode("utf-8")

            text = '%s ' % (barcode_data)

            return text
