import RPi.GPIO as GPIO  
import time  
from functions import *
from definitions import *

def main():
    try:
        # Define the GPIO pins for TRIG and ECHO
        TRIG = 25
        ECHO = 26

        # Set up the TRIG as output and ECHO as input
        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        # Define servo pins
        servos = {
            "base": 4,
            "shoulder": 16,
            "elbow": 21,
            "wrist": 7,
            "gripper": 8
        }

        # Set up servo pins and PWM channels with a frequency of 50Hz
        pwm = {name: GPIO.PWM(pin, 50) for name, pin in servos.items()}
        for p in pwm.values():
            p.start(0)

        # Main loop
        while True:
            # Perform tasks and robot logic
            forward()
            right_turn()
            forward()
            forward_cross(2)
            
            # Measure distance and decide actions
            dist = measure_distance()
            if dist <= 20:
                pick_object()
                reverse()

    except KeyboardInterrupt:
        # Cleanup on exit
        stop()
        for p in pwm.values():
            p.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
