import sys
sys.path.insert(0,'/classes')
from classes.timingController import TimingController
from classes.followController import FollowController
from classes.holeController import HoleController, PHASE_1, PHASE_2, PHASE_3, PHASE_4, PHASE_5
from classes.junctionController import JunctionController
from movementInstructionController import MovementInstructionController
from sensorController import SensorController
from speedController import SpeedController
from util.oled import clear_display, print_motor_speed, print_movement_instruction, update_display, print_countdown
from util.sensoren import query_sensor
import time

HARD_LEFT = 'hard left'
MEDIUM_LEFT = 'medium left'
LEFT = 'left'

FORWARD = 'forward'

RIGHT = 'right'
MEDIUM_RIGHT = 'medium right'
HARD_RIGHT = 'hard right'

STOP = 'stop'
BACKWARD = 'backward'


class NiBot:
    def __init__(self, print_speed=False, debug=False, speed_controller=SpeedController()):
        self.debug_enabled = debug
        if self.debug_enabled:
            self.__debug_timer = TimingController()
        self.print_speed_enabled = print_speed

        self.__speed_controller = speed_controller
        self.__sensor_data = SensorController()
        self.__instructions = MovementInstructionController(self.__sensor_data)

        # Current Movement Speed Instructions
        self.__direction = FORWARD

        self.__junction_controller = None
        self.__follow_controller = None
        self.__hole_controller = None
        # junction right turn until left sensors are white

        # Play Countdown
        self.__play_countdown_delay = 2

    def __debug(self, *value):
        if not self.debug_enabled:
            return
        if not isinstance(self.__debug_timer, TimingController):
            self.__debug_timer = TimingController()
        if self.__debug_timer.seconds_since_start() < 1:
            return

        print('[debug]', value)
        self.__debug_timer.reset_timer()

    def __update_display_values(self):
        if not self.print_speed_enabled:
            return

        clear_display()

        # Update the displayed motor speed and movement instruction
        print_motor_speed(speed_r=self.__speed_controller.get_current_speed_right(),
                          speed_l=self.__speed_controller.get_current_speed_left())
        print_movement_instruction(self.__direction)

        update_display()

    def play_start_countdown(self):
        time.sleep(self.__play_countdown_delay)
        print_countdown("3", 0)
        time.sleep(self.__play_countdown_delay)
        print_countdown("2", 5)
        time.sleep(self.__play_countdown_delay)
        print_countdown("1", 10)
        time.sleep(self.__play_countdown_delay)
        print_countdown('Start!', 15)

    def set_left_motor_speed(self, speed):
        self.__debug("left", speed)
        self.__speed_controller.set_speed_left(speed)

    def set_right_motor_speed(self, speed):
        self.__debug("right", speed)
        self.__speed_controller.set_speed_right(speed)

    def __get_turn_left_motor_speed(self):
        if self.__instructions.medium_left:
            return self.__speed_controller.get_slow_turn_speed()
        elif self.__instructions.left:
            return self.__speed_controller.get_medium_speed()
        else:
            return self.__speed_controller.get_hard_turn_braking_speed()

    def __get_turn_right_motor_speed(self):
        if self.__instructions.medium_right:
            return self.__speed_controller.get_slow_turn_speed()
        elif self.__instructions.right:
            return self.__speed_controller.get_medium_speed()
        else:
            return self.__speed_controller.hard_turn_breaking_speed

    def __update_left_direction(self):
        if self.__instructions.left:
            self.__direction = LEFT
        elif self.__instructions.medium_left:
            self.__direction = MEDIUM_LEFT
        else:
            self.__direction = HARD_LEFT

    def __update_right_direction(self):
        if self.__instructions.right:
            self.__direction = RIGHT
        elif self.__instructions.medium_right:
            self.__direction = MEDIUM_RIGHT
        else:
            self.__direction = HARD_RIGHT

    def __turn_left(self):
        self.__speed_controller.set_speed(
            left=self.__get_turn_left_motor_speed(),
            right=self.__speed_controller.get_max_speed()
        )
        self.__update_left_direction()

    def __turn_right(self):
        self.__speed_controller.set_speed(
            left=self.__speed_controller.get_max_speed(),
            right=self.__get_turn_right_motor_speed()
        )
        self.__update_right_direction()

    def __rotate_left(self):
        self.__speed_controller.set_speed(
            left=-self.__speed_controller.get_max_speed(),
            right=self.__speed_controller.get_max_speed()
        )
    
    def __rotate_right(self):
        self.__speed_controller.set_speed(
            left=self.__speed_controller.get_max_speed(),
            right=-self.__speed_controller.get_max_speed()
        )

    def stop(self):
        self.__speed_controller.set_speed(left=0, right=0)
        self.__direction = STOP

    def drive_forward(self):
        self.__speed_controller.set_speed(
            left=self.__speed_controller.get_max_speed(),
            right=self.__speed_controller.get_max_speed()
        )
        self.__direction = FORWARD

    def drive_backward(self):
        self.__speed_controller.set_speed(
            left=-self.__speed_controller.get_max_speed(),
            right=-self.__speed_controller.get_max_speed()
        )
        self.__direction = BACKWARD

    def __init_junction_controller(self):
        self.__junction_controller = JunctionController()
        self.__hole_controller = None
        self.__follow_controller = None

    def __drive_junction(self):
        if not isinstance(self.__junction_controller, JunctionController):
            self.__init_junction_controller()

        if not self.__sensor_data.get_sensor_value_ll():
            self.__junction_controller.set_junction_attempt_lost_black()

        self.__turn_right()

    def __drive_half_junction_l(self):
        self.__turn_left()

    def __drive_half_junction_r(self):
        self.__turn_right()

    def __init_drive_hole(self):
        self.__hole_controller = HoleController()
        self.__junction_controller = None
        self.__follow_controller = None

    """
    PHASE_1:Drive forward
    PHASE_2:Stop
    PHASE_3:Drive backward
    PHASE_4:Rotate to the left until the robot finds the black line again | 
            Robot will stay in this phase until the black line is not visable for the outer sensor anymore
    PHASE_5:Ends PHASE_4 which will lead to the end of the left rotation 
    """
    def __drive_hole(self):
        if not isinstance(self.__hole_controller, HoleController):
            self.__init_drive_hole()

        if self.__hole_controller.is_phase(PHASE_1):
            self.drive_forward()
            if self.__hole_controller.is_phase_complete():
                self.__hole_controller.set_phase(PHASE_2)
                self.stop()

        elif self.__hole_controller.is_phase(PHASE_2):
            if self.__hole_controller.is_phase_complete():
                self.__hole_controller.set_phase(PHASE_3)
                self.drive_backward()

        elif self.__hole_controller.is_phase(PHASE_3):
            if self.__hole_controller.is_phase_complete() or self.__sensor_data.can_detect_black():
                self.__hole_controller.set_phase(PHASE_4)
                self.__rotate_left()

        elif self.__hole_controller.is_phase(PHASE_4):
            if not self.__sensor_data.can_detect_black():
                self.__hole_controller.set_lost_sight()

            if self.__hole_controller.has_lost_sight() and self.__sensor_data.can_detect_black():
                self.__hole_controller.set_phase(PHASE_5)

    def __init_drive_follow(self):
        self.__follow_controller = FollowController()
        self.__junction_controller = None
        self.__hole_controller = None

    def __drive_follow(self):
        if not self.__follow_controller:
            self.__init_drive_follow()

        self.__update_movement_instructions()
        self.__update_motor_by_movement_instructions()

    def __update_motor_by_movement_instructions(self):
        if self.__instructions.left or self.__instructions.medium_left or self.__instructions.hard_left:
            self.__turn_left()

        elif self.__instructions.right or self.__instructions.medium_right or self.__instructions.hard_right:
            self.__turn_right()

        else:
            self.drive_forward()

    def __update_movement_instructions(self):
        self.__debug('updateing movement instructions')

        self.__instructions.update(self.__sensor_data)

        self.__debug(
            "begin loop: ",
            HARD_LEFT if self.__instructions.hard_left else 0,
            MEDIUM_LEFT if self.__instructions.medium_left else 0,
            LEFT if self.__instructions.left else 0,
            FORWARD if self.__instructions.forward else 0,
            RIGHT if self.__instructions.right else 0,
            MEDIUM_RIGHT if self.__instructions.medium_right else 0,
            HARD_RIGHT if self.__instructions.hard_right else 0
        )

    def __update_sensor_values(self):
        self.__sensor_data.set_sensor_values(query_sensor())
        self.__debug('sensor_values: ', self.__sensor_data.get_sensor_values())

    def __should_force_drive_junction(self):
        return \
            isinstance(self.__junction_controller, JunctionController) \
            and not self.__junction_controller.get_junction_attempt_lost_black()

    def __should_force_drive_hole(self):
        return \
            isinstance(self.__hole_controller, HoleController) \
            and (self.__hole_controller.is_phase(PHASE_3) \
                or self.__hole_controller.is_phase(PHASE_4))

    def run(self):

        if self.print_speed_enabled:
            self.__update_display_values()

        self.__update_sensor_values()

        # Detect
        detect_junction = self.__sensor_data.is_junction()
        detect_half_junction_l = self.__sensor_data.is_half_junction_l()
        detect_half_junction_r = self.__sensor_data.is_half_junction_r()
        detect_hole = self.__sensor_data.is_hole()
        detect_follow = self.__sensor_data.is_follow()

        self.__debug("detect_junction", detect_junction)
        self.__debug("detect_half_junction_l", detect_half_junction_l)
        self.__debug("detect_half_junction_r", detect_half_junction_r)
        self.__debug("detect_hole", detect_hole)
        self.__debug("detect_follow", detect_follow)

        if self.__should_force_drive_junction():
            self.__drive_junction()
            return

        if self.__should_force_drive_hole():
            self.__drive_hole()
            return

        if detect_follow:
            self.__drive_follow()

        if detect_junction:
            self.__drive_junction()

        if detect_half_junction_l:
            self.__drive_half_junction_l()

        if detect_half_junction_r:
            self.__drive_half_junction_r()

        if detect_hole:
            self.__drive_hole()
