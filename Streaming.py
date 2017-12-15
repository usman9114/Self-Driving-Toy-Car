__author__ = 'zhengwang'

import numpy as np
import cv2
import socket
from stop import detect_sign
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8081))
server_socket.listen(1)
connection, client_address = server_socket.accept()
connection = connection.makefile('rb')



def stream_video():

    try:
        print ("Connection from: ", client_address)
        print ("Streaming...")
        print ("Press 'q' to exit")

        stream_bytes = bytes()


        while True:


            stream_bytes += connection.read(1024)
            first = stream_bytes.find(b'\xff\xd8')
            last = stream_bytes.find(b'\xff\xd9')

            if first != -1 and last != -1:
                jpg = stream_bytes[first:last + 2]
                stream_bytes = stream_bytes[last + 2:]
                image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
               # roi = image[197:320, 50:500]
                image,_=detect_sign(image)
                image = cv2.resize(image,(128,128))

                cv2.imshow('edged', image)


                if cv2.waitKey(25) & 0xFF == ord('q'):
                    break
    finally:
        connection.close()
        server_socket.close()
stream_video()





