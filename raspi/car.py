
#!/usr/bin/python             # This is server.py file
import socket                 # Import socket module
import time
import pigpio
import sys
#################### GPIO OUT PINS
pi = pigpio.pi()
#using BCM mode
esc = 27
servo = 4
#####################

pi.set_servo_pulsewidth(servo,1500)
pi.set_servo_pulsewidth(esc,0)


current_pos = 1500


def forward():
    forward_staright()
    pi.set_servo_pulsewidth(27,1970)
    #time.sleep(0.15)
    
    
def forward_staright():
    pi.set_servo_pulsewidth(servo,1500)
    global current_pos
    current_pos = 1500


#def forward_left():
   
   # GPIO.output(motorback_2,False)
    

#def forward_right():
    
    #GPIO.output(motorback_2,False)
   
    

def backward():
   
    pi.set_servo_pulsewidth(27,1600)
    time.sleep(0.05)


def left():
    global current_pos
    if current_pos >=1200:
        for pos in range (1,3):
            current_pos -=50
            time.sleep(0.06)
    pi.set_servo_pulsewidth(4,current_pos)
    pi.set_servo_pulsewidth(esc,1950)
    

def right():
    global current_pos
    if current_pos <= 1850 :
        for pos in range (1,3):
            current_pos +=50
            time.sleep(0.07)
    pi.set_servo_pulsewidth(4,current_pos)
    pi.set_servo_pulsewidth(esc,1950)



def clean():
    pi.set_servo_pulsewidth(servo,0)
    pi.set_servo_pulsewidth(esc,0)


def brake():
    pi.set_servo_pulsewidth(esc,0)

def sign():
    pi.set_servo_pulsewidth(esc,1800)
    time.sleep(0.4)
    pi.set_servo_pulsewidth(esc,0)

      
def stop():
    pi.set_servo_pulsewidth(esc,0)   

s = socket.socket()           # Create a socket object
host = "0.0.0.0"              # Get local machine name
port = 12344                  # Port
s.bind((host, port))          # Bind to the port
s.listen(5)                   # Now wait for client connection.
print ("Listening")
c, addr = s.accept()          # Establish connection with client.

drive ={'forw':forward,
        #'fors':forward_staright,
        'left':left,
        'righ':right,
        #'forward_left':forward_left,
        #'forward_right':forward_right,
        'reve':backward,
        'brak':brake,
        'exit':stop,
        'sign':sign
        }   


try:
 while True:
    data = c.recv(1024)
    msg = data.decode('utf-8')

    #print ('Got connection from', addr)
    
    if msg != 'brak':
        print(msg[:4])
    try:
        drive[msg[:4]]()
    except Exception as e:
        print(e)
        clean()
        c.close()
        print("Car connection closed")
        sys.exit()

    
except KeyboardInterrupt:
    pass
    
finally:
    c.close()
    clean()
    print("Car connection closed")











