import schedule 
import time 
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

left = 17
right = 4
timeToWake = "05:15"
timeToWakeWeekend = "08:00"
timeToWake = timeToWakeWeekend

GPIO.setup(left, GPIO.OUT)
GPIO.setup(right, GPIO.OUT)
  
# Functions setup 
def wakeUp(): 
    GPIO.output(right, GPIO.HIGH)
    time.sleep(900)
    GPIO.output(left, GPIO.HIGH)

#def sleep():
   # GPIO.output(right, GPIO.LOW)
    #time.sleep(900)
    #GPIO.output(left, GPIO.LOW)
  
# Every day at 12am or 00:00 time bedtime() is called
schedule.every().monday.at(timeToWake).do(wakeUp)
schedule.every().tuesday.at(timeToWake).do(wakeUp)
schedule.every().wednesday.at(timeToWake).do(wakeUp)
schedule.every().thursday.at(timeToWake).do(wakeUp)
schedule.every().friday.at(timeToWake).do(wakeUp)
schedule.every().saturday.at(timeToWakeWeekend).do(wakeUp)
schedule.every().sunday.at(timeToWakeWeekend).do(wakeUp)
#schedule.every().day.at("20:15").do(sleep) 
  
# Every tuesday at 18:00 sudo_placement() is called 
#schedule.every().tuesday.at("18:00").do(sudo_placement) 
  
# Loop so that the scheduling task 
# keeps on running all time. 
while True: 
  
    # Checks whether a scheduled task  
    # is pending to run or not 
    schedule.run_pending() 
    time.sleep(1) 
