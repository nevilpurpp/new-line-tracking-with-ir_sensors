from definitions import *



def set_servo_angle(servo_name, angle):
    duty_cycle = 2 + (angle / 18)
    pwm[servo_name].ChangeDutyCycle(duty_cycle)
    time.sleep(0.5)  # Wait for the servo to reach the position
    pwm[servo_name].ChangeDutyCycle(0)  # Turn off PWM signal to stop jitter

def pick_object():
    # Define the sequence of movements for picking up an object
    # Adjust these angles as per your robotic arm's configuration
    set_servo_angle("base", 90)      # Rotate base to the object
    set_servo_angle("shoulder", 45)  # Move shoulder down to reach the object
    set_servo_angle("elbow", 90)     # Adjust elbow to reach the object
    set_servo_angle("wrist", 0)      # Position wrist for picking
    set_servo_angle("gripper", 30)   # Open gripper

    time.sleep(1)  # Wait for a moment to ensure the arm is in position

    set_servo_angle("gripper", 90)   # Close gripper to grasp the object

    time.sleep(1)  # Ensure the object is gripped

    set_servo_angle("shoulder", 90)  # Lift the object
    set_servo_angle("elbow", 45)     # Adjust elbow to lift the object
    set_servo_angle("wrist", 90)     # Adjust wrist to lift the object

    time.sleep(1)  # Wait for the arm to stabilize

def place_object():
    set_servo_angle("base", 0)       # Rotate base to the target position
    set_servo_angle("shoulder", 45)  # Move shoulder down to place the object
    set_servo_angle("elbow", 90)     # Adjust elbow to place the object
    set_servo_angle("wrist", 0)      # Position wrist for placing
    set_servo_angle("gripper", 30)   # Open gripper to release the object

    time.sleep(1)  # Ensure the object is released

    # Return to the initial position
    set_servo_angle("shoulder", 90)
    set_servo_angle("elbow", 90)
    set_servo_angle("wrist", 90)
    set_servo_angle("gripper", 0)
    time.sleep(1)  # Wait for the arm to stabilize

def measure_distance():
    # Send a 10µs pulse to TRIG to start the measurement
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for the ECHO pin to go high and record the start time
    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    # Wait for the ECHO pin to go low and record the end time
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # Calculate the duration of the pulse
    pulse_duration = end_time - start_time

    # Calculate the distance in cm (speed of sound is 34300 cm/s)
    distance = (pulse_duration * 34300) / 2
    return distance    

def set_speed(motorA_speed, motorB_speed):
    pwmA.ChangeDutyCycle(motorA_speed)
    pwmB.ChangeDutyCycle(motorB_speed)

def move_forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def sensor_readings():
    
    # Read sensor values (1 means white line detected, 0 means black surface)
    s1 = GPIO.input(SENSOR1)
    s2 = GPIO.input(SENSOR2)
    s3 = GPIO.input(SENSOR3)
    s4 = GPIO.input(SENSOR4)
    s5 = GPIO.input(SENSOR5)
    return [s1, s2, s3, s4, s5]


def calculate_error(sensor_values):
    # Assign weights to sensors: [leftmost, left, center, right, rightmost]
    WEIGHTS = [-2, -1, 0, 1, 2]
    error = sum(weight * value for weight, value in zip(WEIGHTS, sensor_values))
    return error

def forward():
    global previous_error, integral, previous_time
    
    while True:
        sensor_values = sensor_readings()
        error = calculate_error(sensor_values)
        # Print the error
        print(f"Sensor values: {sensor_values}, Error: {error}")
        
        current_time = time.time()
        dt = current_time - previous_time

        proportional = error
        integral += error * dt
        derivative = (error - previous_error) / dt if dt > 0 else 0

        correction = (KP * proportional) + (KI * integral) + (KD * derivative)

        left_speed = BASE_SPEED - correction
        right_speed = BASE_SPEED + correction

        # Clamp the speeds between 0 and 100
        left_speed = max(min(left_speed, 100), 0)
        right_speed = max(min(right_speed, 100), 0)

        print(f"Correction: {correction}, Left speed: {left_speed}, Right speed: {right_speed}")

        GPIO.output(IN1, GPIO.LOW)
        GPIO.output(IN2, GPIO.HIGH)
        GPIO.output(IN3, GPIO.LOW)
        GPIO.output(IN4, GPIO.HIGH)
        set_speed(left_speed, right_speed)

        previous_error = error
        previous_time = current_time
        



def forward_cross(c):
    sensor_values = sensor_readings()
    cross = 0
   
    while cross < c:
        # Forward movement
        line_following()

        # Check if all IR sensors detect white line
        if all(value == 1 for value in sensor_values):  # Junction detected
            # Stop for 100 milliseconds
            stop()
            time.sleep(0.5)
            # Increment cross count
            cross += 1
            # Print cross count
            print(cross)


def right_turn():
    # Make a right turn based on sensor readings
    while True:
        sensor_values = sensor_readings()
        if all(value == 1 for value in sensor_values):  # Junction detected
            stop()
            time.sleep(0.1)
            # Move forward a bit before turning
            move_forward()
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)
            stop()
            time.sleep(0.1)
            # Execute right turn
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)  # Adjust the sleep time based on your turn requirement
            stop()
            break
        elif sensor_values == [0, 0, 1, 1, 1]:  # Example condition for turning right
            GPIO.output(IN1, GPIO.HIGH)
            GPIO.output(IN2, GPIO.LOW)
            GPIO.output(IN3, GPIO.LOW)
            GPIO.output(IN4, GPIO.HIGH)
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)  # Adjust the sleep time based on your turn requirement
            stop()
            break

def left_turn():
    # Make a left turn based on sensor readings
    while True:
        sensor_values = sensor_readings()
        if all(value == 1 for value in sensor_values):  # Junction detected
            stop()
            time.sleep(0.1)
            # Move forward a bit before turning
            move_forward()
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)
            stop()
            time.sleep(0.1)
            # Execute left turn
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)  # Adjust the sleep time based on your turn requirement
            stop()
            break
        elif sensor_values == [1, 1, 1, 0, 0]:  # Example condition for turning left
            GPIO.output(IN1, GPIO.LOW)
            GPIO.output(IN2, GPIO.HIGH)
            GPIO.output(IN3, GPIO.HIGH)
            GPIO.output(IN4, GPIO.LOW)
            set_speed(BASE_SPEED, BASE_SPEED)
            time.sleep(0.5)  # Adjust the sleep time based on your turn requirement
            stop()
            break


def reverse():
    """
    this function implements a reverse logic"""
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)


  