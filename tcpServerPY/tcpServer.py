# Echo server program
import socket
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

left = 17
right = 4
#dimm = 12

GPIO.setup(left, GPIO.OUT)
GPIO.setup(right, GPIO.OUT)
#dimm = GPIO.PWM(dimm, 100)
#dimm.start(0)

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 8080              # Arbitrary non-privileged port
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))            # Bind host and port to server
    print('Server started')
    while True:                 # Keep in a loop since if connection is broken, server will turn off
        s.listen(1)             # Listen to the socket
        conn, addr = s.accept()         # Accept incoming request to connect
        with conn:
            while True:
                leftstate = GPIO.input(left)        # Read the state of pin number, 1/0 True/False
                rightstate = GPIO.input(right)
                data = conn.recv(1024)                          # Recieve a maximum of 1024 bits from the stream
                data = data.decode('ASCII')                     # Decode the recevied from ASCII code to normal code
                if (data == 'nigg' and leftstate == False):     # Turn on the left lights
                    GPIO.output(left, GPIO.HIGH)
                elif (data == 'nigg' and leftstate == True) :   # Turn off the left lights
                    GPIO.output(left, GPIO.LOW)
                elif (data == 'Letto' and rightstate == False):    # Turn on the right lights
                    GPIO.output(right, GPIO.HIGH)
                elif (data == 'Letto' and rightstate == True) :  # Turn off the right ligths
                    GPIO.output(right, GPIO.LOW)
                elif (data == 'BOTH' and leftstate == False and rightstate == False):     # Turn either both lights on 
                    GPIO.output(left, GPIO.HIGH)
                    GPIO.output(right, GPIO.HIGH)
                elif (data == 'BOTH' and (leftstate == True or rightstate == True)) :   # Turn either both lights off
                    GPIO.output(left, GPIO.LOW)
                    GPIO.output(right, GPIO.LOW)
                    
                if not data: break                              # If connection is lost, or no data is recevied. Close server.
                print(data)
                