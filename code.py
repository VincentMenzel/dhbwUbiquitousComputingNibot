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


while True:

    print("begin loop: ", int(hard_left), left, forward, right, hard_right)

    # Read the sensor Values.
    sensorWerte = sensorAbfrage()
    sensorWert_RR = sensorWerte[4]
    sensorWert_R = sensorWerte[3]
    sensorWert_M = sensorWerte[2]
    sensorWert_L = sensorWerte[1]
    sensorWert_LL = sensorWerte[0]

    print('sensorwert: ', sensorWerte)

    # Update the movement instructions if any sensor detects the black line
    # If the black line is detected nowhere the robot continues it's current instructions.
    if 1 in sensorWerte:

        print('updated movement instructions')
        forward = bool(sensorWert_M)

        left  = bool(sensorWert_L or sensorWert_LL)
        hard_left = bool(sensorWert_LL)

        right = bool(sensorWert_R or sensorWert_RR)
        hard_right = bool(sensorWert_RR)


    clear_display()

    if left:

        motor_left_speed = 0 if hard_left or not forward else slow_turn_speed 
        motor_right_speed = max_turn_speeed if hard_left else max_speed
        
        # Drive turn with max_turn speed if a sharp turn is required
        motorR(motor_right_speed)

        # Stop the left motor if a sparp turn is required. 
        # Otherwise only slow the motor to the in the slow turn multiplier defined speed
        motorL(motor_left_speed)

        print("drive left", ('l:', motor_left_speed), ('r:', motor_right_speed))
        print_motor_speed(speed_r=motor_right_speed, speed_l=motor_left_speed)
        print_movement_instrcution('left' if not hard_left else 'hard left')

    elif right: 

        motor_left_speed = max_turn_speeed if hard_right else max_speed
        motor_right_speed = 0 if hard_right or not forward else slow_turn_speed

        # Drive turn with max_turn speed if a sharp turn is required
        motorR(motor_right_speed)

        # Stop the right motor if a sparp turn is required. 
        # Otherwise only slow the motor to the in the slow turn multiplier defined speed
        motorL(motor_left_speed)

        print("drive right", ('l:', motor_left_speed), ('r:', motor_right_speed))
        print_motor_speed(speed_r=motor_right_speed, speed_l=motor_left_speed)
        print_movement_instrcution('right' if not hard_right else 'hard right')
    else:
        motorR(max_speed)
        motorL(max_speed)
        print("drive forward",('l:', max_speed), ('r:', max_speed) )
        print_motor_speed(speed_r=max_speed, speed_l=max_speed)
        print_movement_instrcution('forward')

    update_display()
    print('end   loop: ' ,hard_left, left, forward, right, hard_right)