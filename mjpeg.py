import cv2
from urllib.request import  urlopen
import numpy as np
from stop import detect_sign,detect_car
global image
stream = urlopen('http://192.168.137.8:8080/stream/video.mjpeg')
bytes = bytes()
while True:
    bytes += stream.read(1024)
    a = bytes.find(b'\xff\xd8')
    b = bytes.find(b'\xff\xd9')
    if a != -1 and b != -1:
        jpg = bytes[a:b + 2]
        bytes = bytes[b + 2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

        car, mmidCar = detect_car(i)
        streamCam, midSign = detect_sign(i)

        cv2.imshow('roi', streamCam)
        if cv2.waitKey(1) == 27:
            exit(0)