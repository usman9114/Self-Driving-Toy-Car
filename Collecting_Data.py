import socket
import time
from os import getcwd

import cv2
import numpy as np

from get_keys import key_check

#s = socket.socket()         # Create a socket object
host = "192.168.137.8"
port = 12344          # port
#s.connect((host,port))

#server_socket = socket.socket()
#server_socket.bind(('0.0.0.0', 8081))
#server_socket.listen(0)
#connection, client_address = server_socket.accept()
#connection = connection.makefile('rb')


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(1)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('0.0.0.0', 8081))
server.listen(2)



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))

connection, client_address = server.accept()
connection = connection.makefile('rb')

recordfile  = getcwd()+"\\frame_record.txt"


def main():
    for i in list(range(4))[:: -1]:
        print(i+1)
        time.sleep(0.25)
        last_time = time.time()

        try:
            print ("Connection from: ", client_address)
            print ("Streaming...")
            print ("Press 'q' to exit")
            stream_bytes = bytes()

            with open(recordfile,'r') as getFrame:
                frame = int(getFrame.read())
                getFrame.close()

            while True:
                stream_bytes += connection.read(4024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
                    roi = image[197:320, 50:500]



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
            connection.close()
            #server_socket.close()
            s.close()
main()
