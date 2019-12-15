import cv2


capture = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')

while True:
    ret, frame = capture.read()

    if ret:
        face = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(face, 1.3, 5)

        print(len(faces))

        for (x, y, w, h) in faces:
            rectFace = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 10)

        cv2.imshow('RectangleInMyface', rectFace)

        if cv2.waitKey(1) & 0xff == 27:
            break

capture.release()
cv2.destroyAllWindows()