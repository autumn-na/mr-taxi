import numpy as np
import cv2
from PIL import Image
import http.client, urllib.request, urllib.parse, urllib.error, base64, json



def print_text(json_data):
    result = json.loads(json_data)
    for l in result['regions']:
        for w in l['lines']:
            line = []
            for r in w['words']:
                line.append(r['text'])
            a = (''.join(line))
            print(a)
    return


def ocr_project_oxford(headers, params, data):
    #HTTP메소드를 통해서 request주소를 적은다음
    conn = http.client.HTTPSConnection('westcentralus.api.cognitive.microsoft.com')
    conn.request("POST", "/vision/v1.0/ocr?%s" % params, data, headers)
    response = conn.getresponse()
    data = response.read().decode()
    print(data + "\n")
    print_text(data)
    conn.close()
    return

def order_points(pts):
    #initialzie a list of coordinates that will be ordered
    #such that the first entry in the list is the top-left
    #the second entry in the top-right the third is the
    #bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4,2), dtype= "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    diff = np.diff(pts, axis= 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    return rect

def auto_scan_image_via_webcam():

    global warped
    try:
        cap = cv2.VideoCapture(0)
    except:
        print('cammot load camera')
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print('connot laod camera!')
            break

        k = cv2.waitKey(10)
        if k == 27:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (3,3), 0)
        edged = cv2.Canny(gray, 75, 200)
        #findContours를 통해 contours들을 반환받음

        print("Step 1: edge detection")
        (cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        #반환 받은 contour를 외곽이 그린 면적이 큰 순서대로 정렬해서 5개를 받음
        cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

        #그렇게 받아온 contour를 순차적으로 탐색하면서
        for c in cnts:
            peri = cv2.arcLength(c, True)#contour가 그리는 길이를 반환
            approx = cv2.approxPolyDP(c, 0.02 * peri, True) #그 길이에 2% 정도 오차를 해서 approxPolyDP를 통해 도형을 조금 근사해서 구함
            screenCnt = []

            if len(approx) == 4:
                contourSize = cv2.contourArea(approx)
                camSize = frame.shape[0] * frame.shape[1]
                ratio = contourSize / camSize

                if ratio > 0.1:
                    screenCnt = approx
                break

        if len(screenCnt) == 0:
            cv2.imshow("WebCam", frame)
            continue
        else:
            print("STEP 2: Find contours of paper")

            cv2.drawContours(frame, [screenCnt], -1, (0,255,0), 2)
            cv2.imshow("WebCam", frame)

            rect = order_points(screenCnt.reshape(4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = rect

            w1 = abs(bottomRight[0] - bottomLeft[0])
            w2 = abs(topRight[0] - topLeft[0])
            h1 = abs(topRight[1] - bottomRight[1])
            h2 = abs(topLeft[1] - bottomLeft[1])
            maxWidth = max([w1, w2])
            maxHeight = max([h1, h2])

            dst = np.float32([[0,0], [maxWidth-1,0],
                              [maxWidth-1,maxHeight-1], [0,maxHeight-1]])
            M = cv2.getPerspectiveTransform(rect, dst)
            warped = cv2.warpPerspective(frame, M, (maxWidth,maxHeight))

            print("step 3: apply perspective trasnform")
            warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
            warped = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, 10)

            print("Step 4: apply adaptive threshold")
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

    cv2.imshow("Scanned", warped)
    cv2.imwrite("scannedImage.png", warped)

    headers = {
        #헤더요청
        # hearders Free Key를 추가
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '1f6ac2b85e584583843f8c3ca307174d', #project oxford 인증키 입력
    }
    params = urllib.parse.urlencode({
     #파라미터 요청
     # language경우 unknown을 넣어서 자동으로 언어입력
     # daterOrientaton은 글자의 각도까지 감지
        'language': 'unk',
        'detectOrientation ' : 'true',
    })
    data = open("scannedImage.png", 'rb').read()

    try:
        image_file = "scannedImage.png"
        ocr_project_oxford(headers, params, data)
    except Exception as e:
        print(e)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.waitKey(1)

if __name__ == "__main__":
    auto_scan_image_via_webcam()



