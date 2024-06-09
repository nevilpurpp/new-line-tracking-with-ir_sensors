import RPi.GPIO as GPIO
import time

# GPIO pin assignments for motors
IN1 = 17
IN2 = 18
ENA = 27
IN3 = 22
IN4 = 23
ENB = 24

# GPIO pin assignments for IR sensors
SENSOR1 = 5
SENSOR2 = 6
SENSOR3 = 13
SENSOR4 = 20
SENSOR5 = 19

# PID Controller parameters
KP = 12  # Proportional gain
KI = 0.1  # Integral gain
KD = 10  # Derivative gain
BASE_SPEED = 50  # Base speed for motors (0 to 100)

previous_error = 0
integral = 0
previous_time = time.time()

'''
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
'''