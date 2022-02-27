from oled import clear_display, print_countdown, print_motor_speed, print_movement_instruction, update_display
from motor import *
from sensoren import *


def get_time_diff_in_sec(date1: int, date2: int):
    difference = (date1 - date2)
    return abs(difference)


class NiBot:
    def __init__(self, print_speed=False, debug=False):
        self.debug = debug
        self.print_speed = print_speed
        self.sensor_values = [0, 0, 0, 0, 0]
        self.sensor_value_rr = self.sensor_values[4]
        self.sensor_value_r = self.sensor_values[3]
        self.sensor_value_m = self.sensor_values[2]
        self.sensor_value_l = self.sensor_values[1]
        self.sensor_value_ll = self.sensor_values[0]

    # Define the max speed of the robot. (0 - 100)
    max_speed = 23

    # Define the hard turn multilplier when driving a sharp turn.
    hard_turn_multiplier = 1.25
    hard_turn_breaking = 0

    # Define the slow turn multilplier when driving a soft turn.
    slow_turn_multiplier = .4

    # Calculate sharp turn speed.
    max_turn_speeed = get_valid_speed(max_speed * hard_turn_multiplier)
    slow_turn_speed = get_valid_speed(slow_turn_multiplier * max_speed)

    # Default instructions for movement.
    forward = True
    left = False
    hard_left = False
    right = False
    hard_right = False

    # Current Movement Speed Instructions
    motor_left_speed = max_speed
    motor_right_speed = max_speed
    direction = 'forward'

    junction_attempt_start = False
    hole_attempt_start = False
    drive_attempt_start = False

    hole_attempt_phase = 0
    hole_attempt_turn_lost_sight = False

    # Play Countdown
    delay = 2

    def print(self, *value):
        if not self.debug:
            pass

        print(value)

    def update_display_values(self):
        if not self.print_speed:
            pass

        clear_display()

        # Update the displayed motor speed and movement instruction
        print_motor_speed(speed_r=self.motor_right_speed, speed_l=self.motor_left_speed)
        print_movement_instruction(self.direction)

        update_display()

    def play_start_countdown(self):
        time.sleep(self.delay)
        print_countdown("3", 0)
        time.sleep(self.delay)
        print_countdown("2", 5)
        time.sleep(self.delay)
        print_countdown("1", 10)
        time.sleep(self.delay)
        print_countdown('Start!', 15)

    def left_motor(self, speed):
        print("left", speed)
        self.motor_left_speed = speed
        motorL(self.motor_left_speed)

    def right_motor(self, speed):
        print("right", speed)
        self.motor_right_speed = speed
        motorR(self.motor_right_speed)

    def turn_left(self):
        self.left_motor(self.hard_turn_breaking if self.hard_left or not self.forward else self.slow_turn_speed)
        self.right_motor(self.max_turn_speeed if self.hard_left else self.max_speed)
        self.direction = 'left' if not self.hard_left else 'hard left'

    def turn_right(self):
        self.left_motor(self.max_turn_speeed if self.hard_right else self.max_speed)
        self.right_motor(self.hard_turn_breaking if self.hard_right or not self.forward else self.slow_turn_speed)
        self.direction = 'right' if not self.hard_right else 'hard right'

    def stop(self):
        self.left_motor(0)
        self.right_motor(0)
        self.direction = 'stop'

    def drive_forward(self):
        self.left_motor(self.max_speed)
        self.right_motor(self.max_speed)
        self.direction = 'forward'

    def drive_backward(self):
        self.left_motor(-self.max_speed*1.25)
        self.right_motor(-self.max_speed*1.25)
        self.direction = 'backward'

    def drive_junction(self):
        if not self.junction_attempt_start:
            self.junction_attempt_start = time.time()
            self.hole_attempt_start = False
            self.drive_attempt_start = False

        self.turn_right()

    def drive_hole(self):
        self.print("self.hole_attempt_start", self.hole_attempt_start)
        self.print("self.hole_attempt_phase", self.hole_attempt_phase)
        self.print("self.hole_attempt_turn_lost_sight", self.hole_attempt_turn_lost_sight)
        
        if not self.hole_attempt_start:
            self.hole_attempt_start = time.time()
            self.hole_attempt_phase = 0
            self.junction_attempt_start = False
            self.drive_attempt_start = False

        since_start = get_time_diff_in_sec(self.hole_attempt_start, time.time())
        self.print("since_start", since_start)

        # Drive forward 2s
        if self.hole_attempt_phase == 0:
            self.drive_forward()
            if since_start >= 0.5:
                self.hole_attempt_start = time.time()
                self.hole_attempt_phase = 1
                self.stop()
        # Break
        elif self.hole_attempt_phase == 1:
            if since_start >= 0.5:
                self.hole_attempt_start = time.time()
                self.hole_attempt_phase = 2
                self.drive_backward()

        # Drive Backward 2s
        elif self.hole_attempt_phase == 2:
            if since_start >= 5: #or 1 in self.sensor_values:
                self.hole_attempt_start = time.time()
                self.hole_attempt_phase = 3
                self.hole_attempt_turn_lost_sight = False
                self.turn_left()

        # Turn around
        elif self.hole_attempt_phase == 3:            
            if 1 not in self.sensor_values:
                self.hole_attempt_turn_lost_sight = True
            if self.hole_attempt_turn_lost_sight and 1 in self.sensor_values:
                self.hole_attempt_phase = 0

    def drive_follow(self):
        if not self.drive_attempt_start:
            self.drive_attempt_start = time.time()
            self.junction_attempt_start = False
            self.hole_attempt_start = False

        if 1 in self.sensor_values and 0 in self.sensor_values:

            self.print('updateing movement instructions')

            self.forward = bool(self.sensor_value_m)

            self.left = bool(self.sensor_value_l or self.sensor_value_ll)
            self.hard_left = bool(self.sensor_value_ll)

            self.right = bool(self.sensor_value_r or self.sensor_value_rr)
            self.hard_right = bool(self.sensor_value_rr)
            self.print(
                "begin loop: ",
                'hard left' if self.hard_left else 0,
                'left' if self.left else 0,
                'forward' if self.forward else 0,
                'right' if self.right else 0,
                'hard right' if self.hard_right else 0
            )
            # Find the correct speed according to the current sensor values
            if self.left and not self.right and not self.hard_right:
                self.turn_left()

            elif self.right and not self.left and not self.hard_left:
                self.turn_right()

            else:
                self.drive_forward()

    def run(self):

        if self.print_speed:
            self.update_display_values()



        # Read the sensor Values.
        self.sensor_values = query_sensor()
        self.sensor_value_rr = self.sensor_values[4]
        self.sensor_value_r = self.sensor_values[3]
        self.sensor_value_m = self.sensor_values[2]
        self.sensor_value_l = self.sensor_values[1]
        self.sensor_value_ll = self.sensor_values[0]

        self.print('sensorwert: ', self.sensor_values)

        # Detect
        detect_junction = 0 not in self.sensor_values
        detect_hole = 1 not in self.sensor_values
        detect_follow = 1 in self.sensor_values

        self.print("detect_junction", detect_junction)
        self.print("detect_hole", detect_hole)
        self.print("detect_follow", detect_follow)
        if not self.hole_attempt_phase == 3:
            if detect_follow:
                self.drive_follow()

            if detect_junction:
                self.drive_junction()

        if detect_hole or self.hole_attempt_phase == 3:
            self.drive_hole()


def main():
  robot = NiBot(True, True)
  robot.play_start_countdown()

  while True:
    robot.run()

main()

if __name__ == '__main__':
    main()

    ## --

    #  1 1 1 1 1
    # Abzweigung?
    # -> Rechts 90°grad

    # 0 0 0 0 0
    # Loch
    # -> 2s geradeaus oder bis schwarz
    # -> kein schwarz
    #   -> rückwärts bis schwarz
    #   -> drehung gegen uhrzeigersinn (links r, rechts v) bis schwarz weg und wieder da

    ## --

    # Update the movement instructions if any sensor detects the black line
    # If the black line is detected nowhere the robot continues it's current instructions.
