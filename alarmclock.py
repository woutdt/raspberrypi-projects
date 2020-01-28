#alarmclock
import RPi.GPIO as GPIO
import time
import datetime

LED = 14
BUZZER = 21
MOTION = 23
BUTTON = 15

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED, GPIO.OUT)
GPIO.setup(BUZZER, GPIO.OUT)
GPIO.setup(MOTION, GPIO.IN)
GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def setAlarm(minuten: int, uren: int):
    now = datetime.datetime.now()
    add = datetime.timedelta(hours = uren, minutes = minuten)
    new = now + add
    return new

def now():
    return datetime.datetime.now()

try:    
    def main():
        minuten = input("minuten:    ")
        uren = input("uren:        ")
        
        alarmRange = setAlarm(int(minuten), int(uren))
        
        notQuit = True
    
        snoozeTime = 0
        
        while notQuit == True:
            while now() < alarmRange:
                time.sleep(1)
                left = alarmRange - now()
                leftDisplay = str(left).split('.')
                print(leftDisplay[0], end="\r")
                
                if GPIO.input(BUTTON) == True:
                    print("alarm uitgezet op: {}".format(now()))
                    notQuit == False
                    alarmRange = datetime.MINYEAR()
            
            while now() > alarmRange or now() == alarmRange:
                GPIO.output(BUZZER, True)
                GPIO.output(LED, True)
                
                if GPIO.input(BUTTON) == True:
                    print("alarm uitgezet op: {}".format(now()))
                    GPIO.output(BUZZER, False)
                    GPIO.output(LED, False)
                    notQuit == False
                    alarmRange = datetime.MINYEAR()
                
                if snoozeTime is not 120:
                    snoozeTime += 1
                    snooze = 120 - int(snoozeTime)
                    print("{} seconden voor uitschakelen alarm".format(snooze), end="\r")
                    time.sleep(1)
                    #if motion detected
                
                if snoozeTime == 120:
                    print("\r")
                    print("alarm uitgeschakeld op:")
                    print(now().hour, now().minute, now().second)
                    led = False
                    GPIO.output(LED, False)
                    GPIO.output(BUZZER, False)
                    notQuit = False

                if GPIO.input(MOTION) == True:
                    GPIO.output(BUZZER, False)
                    GPIO.output(LED, False)
                    alarmRange = setAlarm(10, 0)
                    snoozeTime = 0
                    print('\r')
                    print('alarm gesnoozed op: {}'.format(now()))
                    print('\n')

    main()
except:
    GPIO.output(BUZZER, False)
    GPIO.output(LED, False)
    GPIO.remove_event_detect(MOTION)
finally:
    GPIO.cleanup()
