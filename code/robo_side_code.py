import RPi.GPIO as GPIO
import time
import threading
stat_led = 21
data_led = 20
buzzer=16
motor1_fwd = 26
motor1_rev = 19
motor2_fwd = 13
motor2_rev = 6
motor3_fwd = 7
motor3_rev = 8
pwm=12
button=24
def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(stat_led,GPIO.OUT)
    GPIO.setup(data_led,GPIO.OUT)
    GPIO.setup(motor1_fwd,GPIO.OUT)
    GPIO.setup(motor1_rev,GPIO.OUT)
    GPIO.setup(motor2_fwd,GPIO.OUT)
    GPIO.setup(motor2_rev,GPIO.OUT)
    GPIO.setup(pwm,GPIO.OUT)
    GPIO.setup(button,GPIO.IN)
    GPIO.output(motor1_fwd,False)
    GPIO.output(motor2_fwd,False)
    GPIO.output(motor1_rev,False)
    GPIO.output(motor2_rev,False)
    servo=GPIO.PWM(pwm,100)
    servo.start(0)
    threading.Thread(target=buffering).start()
    button_flag=0
    while(True):
        btn_reading=GPIO.input(button)
        if btn_reading==0:
            button_flag=1
            time.sleep(0.5)
            btn_reading=GPIO.input(button)
            if btn_reading==1 and button_flag==1:
                button_flag=0
                for i in range(1,10):
                    vehicle_forward()
                    time.sleep(2)
                    vehicle_stop()
                    time.sleep(0.2)
                    digging()
                    vehicle_forward()
                    time.sleep(1)
                    seed_sowing()
                    time.sleep(0.5)
                vehicle_reverse()
                time.sleep(30)
                vehicle_stop()
                        
                          
def buffering():
    while(1):
        GPIO.output(stat_led,True)
        time.sleep(0.2)
        GPIO.output(stat_led,False)
        time.sleep(0.2)
def vehicle_forward():
    GPIO.output(mot1_fwd,True)
    GPIO.output(mot2_fwd,True)
    GPIO.output(mot1_rev,False)
    GPIO.output(mot2_rev,False)
def vehicle_stop():
    GPIO.output(mot1_fwd,False)
    GPIO.output(mot2_fwd,False)
    GPIO.output(mot1_rev,False)
    GPIO.output(mot2_rev,False)
def vehicle_rev():
    GPIO.output(mot1_fwd,False)
    GPIO.output(mot2_fwd,False)
    GPIO.output(mot1_rev,True)
    GPIO.output(mot2_rev,True)
def digging():
    for i in range(1,10):
        GPIO.output(mot3_fwd,True)
        GPIO.output(mot3_rev,False)
        time.sleep(1)
        GPIO.output(mot3_fwd,False)
        GPIO.output(mot3_rev,False)
        time.sleep(0.2)
        GPIO.output(mot3_fwd,False)
        GPIO.output(mot3_rev,True)
        time.sleep(1)
        GPIO.output(mot3_fwd,False)
        GPIO.output(mot3_rev,False)
        time.sleep(0.2)
def SetAngle(angle):
    duty=angle/18+2
    GPIO.output(pwm,True)
    servo.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(pwm,False)
    servo.ChangeDutyCycle(0)
def seed_sowing():
    for i in range(1,5):
        SetAngle(180)
        time.sleep(0.5)
        SetAngle(0)
        time.sleep(0.5)
if __name__=="__main__":
    main()

