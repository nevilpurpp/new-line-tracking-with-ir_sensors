import RPi.GPIO as GPIO  
import time  
from functions import *
from definitions import *


def main():
    try:

        # Setup GPIO mode
        GPIO.setmode(GPIO.BCM)

# Setup motor pins
        GPIO.setup(IN1, GPIO.OUT)
        GPIO.setup(IN2, GPIO.OUT)
        GPIO.setup(ENA, GPIO.OUT)
        GPIO.setup(IN3, GPIO.OUT)
        GPIO.setup(IN4, GPIO.OUT)
        GPIO.setup(ENB, GPIO.OUT)

# Setup sensor pins
        GPIO.setup(SENSOR1, GPIO.IN)
        GPIO.setup(SENSOR2, GPIO.IN)
        GPIO.setup(SENSOR3, GPIO.IN)
        GPIO.setup(SENSOR4, GPIO.IN)
        GPIO.setup(SENSOR5, GPIO.IN)

# Initialize PWM on ENA and ENB pins
        pwmA = GPIO.PWM(ENA, 1000)  # 100 Hz frequency
        pwmB = GPIO.PWM(ENB, 1000)  # 100 Hz frequency
        pwmA.start(0)  # Start PWM with 0% duty cycle
        pwmB.start(0)  # Start PWM with 0% duty cycle

        #main loop
        while True:
            #perform tasks, and robot logic
            
            forward()
            time.sleep(4)
            right_turn()
  
    except KeyboardInterrupt:
        stop()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()