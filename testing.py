from keras.models import Model, load_model
from os import  getcwd,listdir,environ
environ['TF_CPP_MIN_LOG_LEVEL']='2'

import cv2
import numpy as np
from urllib.request import urlopen
import socket
from stop import detect_sign,detect_car
model_path = getcwd()+'\\best_autopilot(with_car).hdf5'
image =np.array([])

stop_activated = True
stop_time = 0
stop_flag = False
dict = {1: "right", 2: 'left', 0: 'forward'}
num_channel = 1
s = socket.socket()
host = '192.168.137.8'
port = 12344
s.connect((host, port))
def sendCommand(result,prob):

    forward,right,left = prob[0]

    if result == 'forward' :
        s.send('forw'.encode('utf-8'))
        return forward
    elif result == 'left' :
        s.send('left'.encode('utf-8'))
        return left
    elif result == 'right':
        s.send('righ'.encode('utf-8'))
        return right
    elif result == 'stop':
        s.send('sign'.encode('utf-8'))



model = load_model(model_path)




def selfDrive():
    global image
    global bytes , streamCam

    global stop_activated, stop_flag, stop_time

    try:
        print ("Streaming...")
        print ("Press 'q' to exit")

        while True:
                bytes += streamCam.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    #roi = image[197:320, 50:500]
                    roi = image[50:, :]

                    roi = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
                    test_image = cv2.resize(roi, (128, 128))
                    test_image = test_image.astype('float32')
                    test_image /= 255
                    if num_channel == 1:
                        test_image = np.expand_dims(test_image, axis=3)
                        test_image = np.expand_dims(test_image, axis=0)
                    else:
                        test_image = np.expand_dims(test_image,axis=0)

                    result = model.predict_classes(test_image)
                    prob = model.predict(test_image)
                    result = dict[int(result)]
                    #carStream , car_distance = detect_car(image)
                    stream, distance = detect_sign(image)


                    print(distance)

                    if distance >= 50 and stop_activated:
                        print("stoppping")
                        sendCommand('stop',prob)
                        if stop_flag is False:
                            stop_start = cv2.getTickCount()
                            stop_flag = True
                        stop_finish = cv2.getTickCount()
                        stop_time = (stop_finish-stop_start)/cv2.getTickFrequency()
                        print("stop time {}".format(stop_time))

                        if stop_time>5.0:
                            print("moving on")
                            stop_flag = False
                            stop_activated = False
                    #if car_distance >= 170:
                     #   sendCommand('stop',prob)
                    else:
                         probi=sendCommand(result,prob)

                    cv2.putText(stream, result+str(probi), (180, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.imshow('self', stream)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        s.send('exit'.encode('utf-8'))
                        break
    finally:
        s.send('exit'.encode('utf-8'))
        s.close()
streamCam = urlopen('http://192.168.137.8:8080/stream/video.mjpeg')
bytes = bytes()


def main():
    selfDrive()
main()
