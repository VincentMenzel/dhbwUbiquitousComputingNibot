debug = 0
play_radio = 0
# Liniensensor - Robo - Test
# Adafruit CircuitPython 6.2.0
# Board: Metro M4 Express
# Sensoren: Waveshare Tracker Sensor (5x Analog)
# 06.04.21 - vm
# v1.0

# import time
from oled import clear_display, print_countdown, print_motor_speed, print_movement_instruction, update_display
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
hard_turn_multiplier = 2.
hard_turn_breaking = -15

# Define the slow turn multilplier when driving a soft turn. 
slow_turn_multiplier = .7

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


def update_display_values():
    global motor_right_speed
    global motor_left_speed 
    global direction
    clear_display()

    # Update the displayed motor speed and movement instruction
    print_motor_speed(speed_r=motor_right_speed, speed_l=motor_left_speed)
    print_movement_instruction(direction)

    update_display()

def play_start_countdown():
    delay = 2
    time.sleep(delay)
    print_countdown("3", 0)
    time.sleep(delay)
    print_countdown("2", 5)
    time.sleep(delay)
    print_countdown("1", 10)
    time.sleep(delay)
    print_countdown('Start!', 15)

#play_start_countdown()

while True:

    if debug: print("begin loop: ", 'hard left' if hard_left else 0, 'left' if left else 0, 'forward' if forward else 0, 'right' if right else 0, 'hard right' if hard_right else 0)
    #time.sleep(1)

    # Read the sensor Values.
    sensor_values = sensorAbfrage()
    sensor_value_rr = sensor_values[4]
    sensor_value_r= sensor_values[3]
    sensor_value_m = sensor_values[2]
    sensor_value_l = sensor_values[1]
    sensor_value_ll = sensor_values[0]

    if debug: print('sensorwert: ', sensor_values)

    # Update the movement instructions if any sensor detects the black line
    # If the black line is detected nowhere the robot continues it's current instructions.
    if 1 in sensor_values and 0 in sensor_values:

        if debug: print('updateing movement instructions')
        forward = bool(sensor_value_m)

        left  = bool(sensor_value_l or sensor_value_ll)
        hard_left = bool(sensor_value_ll)

        right = bool(sensor_value_r or sensor_value_rr)
        hard_right = bool(sensor_value_rr)


        # Find the correct speed according to the current sensor values
        if left and not right and not hard_right:
       

            motor_left_speed = hard_turn_breaking if hard_left or not forward else slow_turn_speed 
            motor_right_speed = max_turn_speeed if hard_left else max_speed

            direction = 'left' if not hard_left else 'hard left'

        elif right and not left and not hard_left: 

            motor_left_speed = max_turn_speeed if hard_right else max_speed
            motor_right_speed = hard_turn_breaking if hard_right or not forward else slow_turn_speed

            direction = 'right' if not hard_right else 'hard right'

        else:

            motor_left_speed = max_speed
            motor_right_speed = max_speed

            direction = 'forward'


        # Update Right and Left Motor Speed.
        motorR(motor_right_speed)
        motorL(motor_left_speed)


    if play_radio: update_display_values()

    #print('end   loop: ' ,hard_left, left, forward, right, hard_right)