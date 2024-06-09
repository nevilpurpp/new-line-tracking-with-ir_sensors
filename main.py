import RPi.GPIO as GPIO  
import time  
from functions import *
from definitions import *


def main():
    try:

        #main loop
        while True:
            #perform tasks, and robot logic
            
            forward()
            time.sleep(4)
            right_turn()
            measure_distance()
            if distance <= 20:
                pick_object()
                reverse()
            
    except KeyboardInterrupt:
        stop()
        pwmA.stop()
        pwmB.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()