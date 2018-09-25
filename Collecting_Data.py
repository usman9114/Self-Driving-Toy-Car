import socket
import time
from os import getcwd
from urllib.request import  urlopen

import cv2
import numpy as np

from get_keys import key_check

host = "192.168.137.8"
port = 12344          # port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))


recordfile  = getcwd()+"\\frame_record.txt"


def main():
    global bytes,stream
    for i in list(range(4))[:: -1]:
        print(i+1)
        time.sleep(0.25)
        last_time = time.time()

        try:
            print ("Streaming...")
            print ("Press 'q' to exit")

            with open(recordfile,'r') as getFrame:
                frame = int(getFrame.read())
                getFrame.close()

            while True:
                bytes += stream.read(1024)
                a = bytes.find(b'\xff\xd8')
                b = bytes.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    jpg = bytes[a:b + 2]
                    bytes = bytes[b + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    roi = image[50:,]



                    if 'W' in key_check():
                        frame +=1
                        s.send("forw".encode('utf-8'))
                        print("moving forward")
                        cv2.imwrite('training_data_forward/frame{}_{}.jpg'.format(frame,'0'), roi)
                    elif 'D' in key_check():
                        frame +=1
                        s.send("righ".encode('utf-8'))
                        print("moving right")
                        cv2.imwrite('training_data_right/frame{}_{}.jpg'.format(frame,'1'), roi)
                    elif 'A' in key_check():
                        frame +=1
                        s.send("left".encode('utf-8'))
                        print("moving left")
                        cv2.imwrite('training_data_left/frame{}_{}.jpg'.format(frame, '2'), roi)
                    elif 'S' in key_check():
                        s.send("reve".encode('utf-8'))
                        #cv2.imwrite('training_data_forward/frame{}_{}.jpg'.format(frame,'0'), roi)

                        print("moving reverser")

                    else:
                        s.send('brak'.encode('utf-8'))
                    cv2.imshow('video', roi)


                    file = open(recordfile,'w')
                    file.write(str(frame))
                    file.close()

                    print("Frame took {}seconds".format(time.time()-last_time))
                    last_time = time.time()

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break


        finally:
            s.close()
stream = urlopen('http://192.168.137.8:8080/stream/video.mjpeg')
bytes = bytes()
main()
