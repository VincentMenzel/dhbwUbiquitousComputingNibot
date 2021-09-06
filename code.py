# Liniensensor - Robo - Test 1
# Adafruit CircuitPython 6.2.0
# Board: Metro M4 Express
# Sensoren: Waveshare Tracker Sensor (5x Analog)
# 06.04.21 - vm
# v1.0

# import time
from oled import clear_display, print_motor_speed, print_movement_instrcution, update_display
from motor import *
from sensoren import *

# Ensures that the amount passed in is within the valid boundries of the speed.
def get_valid_speed(amount): 
    if amount > 0 and amount < 100:
        return int(amount)
    elif amount < 0:
        return 0
    elif amount > 100:
        return 100


# Define the max speed of the robot. (0 - 100) 
max_speed = 25

# Define the hard turn multilplier when driving a sharp turn. 
hard_turn_multiplier = 1.25

# Define the slow turn multilplier when driving a soft turn. 
slow_turn_multiplier = .5

# Calculate sharp turn speed.
max_turn_speeed = get_valid_speed(max_speed * hard_turn_multiplier)
slow_turn_speed = get_valid_speed(slow_turn_multiplier * max_speed)

# Default instructions for movement.
forward = True
left  = False
hard_left = False
right = False
hard_right = False

# Current Movement Speed Instructions
motor_left_speed = max_speed
motor_right_speed = max_speed
direction = 'forward'


def update_display():
    global motor_right_speed
    global motor_left_speed 
    global direction
    clear_display()

    # Update the displayed motor speed and movement instruction
    print_motor_speed(speed_r=motor_right_speed, speed_l=motor_left_speed)
    print_movement_instrcution(direction)

    update_display()

while True:

    print("begin loop: ", int(hard_left), left, forward, right, hard_right)

    # Read the sensor Values.
    sensor_values = sensorAbfrage()
    sensor_value_rr = sensor_values[4]
    sensor_value_r= sensor_values[3]
    sensor_value_m = sensor_values[2]
    sensor_value_l = sensor_values[1]
    sensor_value_ll = sensor_values[0]

    print('sensorwert: ', sensor_values)

    # Update the movement instructions if any sensor detects the black line
    # If the black line is detected nowhere the robot continues it's current instructions.
    if 1 in sensor_values:

        print('updateing movement instructions')
        forward = bool(sensor_value_m)

        left  = bool(sensor_value_l or sensor_value_ll)
        hard_left = bool(sensor_value_ll)

        right = bool(sensor_value_r or sensor_value_rr)
        hard_right = bool(sensor_value_rr)


        # Find the correct speed according to the current sensor values
        if left:

            motor_left_speed = 0 if hard_left or not forward else slow_turn_speed 
            motor_right_speed = max_turn_speeed if hard_left else max_speed

            direction = 'left' if not hard_left else 'hard left'

        elif right: 

            motor_left_speed = max_turn_speeed if hard_right else max_speed
            motor_right_speed = 0 if hard_right or not forward else slow_turn_speed

            direction = 'right' if not hard_right else 'hard right'

        else:

            motor_left_speed = max_speed
            motor_right_speed = max_speed

            direction = 'forward'


        # Update Right and Left Motor Speed.
        motorR(motor_right_speed)
        motorL(motor_left_speed)


    update_display()

    print('end   loop: ' ,hard_left, left, forward, right, hard_right)