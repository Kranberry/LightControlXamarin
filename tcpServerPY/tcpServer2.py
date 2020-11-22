import socketserver
import RPi.GPIO as GPIO

GPIO.setwarnings(False) #Removes warnings from already in used gpio

GPIO.setmode(GPIO.BCM)  # Sets the layout to BCM layout

left = 17
right = 4
pwm = 13

GPIO.setup(pwm, GPIO.OUT)
p = GPIO.PWM(pwm, 100.0)
p.start(1)
GPIO.setup(left, GPIO.OUT)  #Sets the pin to output
GPIO.setup(right, GPIO.OUT)

def lightControl(command, dimmLevel):
    leftState = GPIO.input(left)    #Looks at the value of the pin, True/False or 1/0
    rightState = GPIO.input(right)
    def leftLight():
        if(leftState == True):
            GPIO.output(left, GPIO.LOW) # Turns pin OFF
        elif(leftState == False):
            GPIO.output(left, GPIO.HIGH)    # Turns pin ON
    def rightLight():
        if(rightState == True):
            GPIO.output(right, GPIO.LOW)
        elif(rightState == False):
            GPIO.output(right, GPIO.HIGH)
    def bothLights():
        if(rightState == True or leftState == True):
            GPIO.output(right, GPIO.LOW)
            GPIO.output(left, GPIO.LOW)
        elif(rightState == False and leftState == False):
            GPIO.output(right, GPIO.HIGH)
            GPIO.output(left, GPIO.HIGH)
    def dimmingLevel(level):
        p.ChangeDutyCycle(level)

    if(command == 'nigg'):      # Decides where we go
        leftLight()
    elif(command == 'Letto'):
        rightLight()
    elif(command == 'BOTH'):
        bothLights()
    elif(command == 'fin'):
        dimmingLevel(dimmLevel)

class tcpHandler(socketserver.BaseRequestHandler):  # Class for handling tcp requests
    def handle(self):
        dimmLevel = 50.0 # Make this be the same as the pwm value
        self.data = self.request.recv(1024).strip() # Recieve data from the socket max 1024 bits
        fdata = self.data.decode('ASCII')   # decode incoming with ASCII
        fdata = fdata.split(';')
        if(fdata[0] == 'fin'):
            dimmLevel = fdata[1]
            lightControl(fdata[0], int(fdata[1]))
           # print(fdata[0] + int(fdata[1]))    # Print data
        else:
            lightControl(fdata[0], dimmLevel)
            print(fdata[0], dimmLevel)    # Print data

if __name__ == "__main__" :
    HOST = ''        #Host ip
    PORT = 8080                 #Port

    server = socketserver.TCPServer((HOST, PORT), tcpHandler)   # Create the socket, bind host and port to server, move to tcpHandler

    server.serve_forever()  # Server stays alive forever, until ctrl+c