"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html
"""
import io
import socket
import struct
import time
import threading
import picamera
import sys

client_socket = socket.socket()
client_socket.connect(('192.168.137.1', 8081))
connection = client_socket.makefile('wb')
try:
    connection_lock = threading.Lock()
    pool_lock = threading.Lock()
    pool = []

    class ImageStreamer(threading.Thread):
        def __init__(self):
            super(ImageStreamer, self).__init__()
            self.stream = io.BytesIO()
            self.event = threading.Event()
            self.terminated = False
            self.start()

        def run(self):
            # This method runs in a background thread
            while not self.terminated:
                
                # Wait for the image to be written to the stream
                if self.event.wait(1):
                    try:
                        with connection_lock:
                            connection.write(struct.pack('<L', self.stream.tell()))
                            connection.flush()
                            self.stream.seek(0)
                            connection.write(self.stream.read())
                            
                                
                    except:
                        connection.close()
                        client_socket.close()
                        print("camera closed")
                        sys.exit()
                    finally:
                        self.stream.seek(0)
                        self.stream.truncate()
                        self.event.clear()
                        with pool_lock:
                            pool.append(self)

    count = 0
    start = time.time()
    finish = time.time()

    def streams():
        global count, finish
        while finish - start < 5*60:
            with pool_lock:
                if pool:
                    streamer = pool.pop()
                else:
                    streamer = None
            if streamer:
                yield streamer.stream
                streamer.event.set()
                count += 1
            else:
                # When the pool is starved, wait a while for it to refill
                time.sleep(0.1)
            finish = time.time()

    with picamera.PiCamera() as camera:
        pool = [ImageStreamer() for i in range(4)]
        camera.resolution = (560, 310)
        camera.framerate = 15
        time.sleep(2)
        start = time.time()
        camera.capture_sequence(streams(), 'jpeg', use_video_port=True)

    # Shut down the streamers in an orderly fashion
    while pool:
        streamer = pool.pop()
        streamer.terminated = True
        streamer.join()

    # Write the terminating 0-length to the connection to let the server
    # know we're done
    with connection_lock:
        connection.write(struct.pack('<L', 0))
except:
    connection.close()
    client_socket.close()
finally:
    connection.close()
    client_socket.close()
    print("camera closed")

print('Sent %d images in %d seconds at %.2ffps' % (
    count, finish-start, count / (finish-start)))
