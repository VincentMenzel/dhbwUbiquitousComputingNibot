from util.motor import motorL, motorR


class SpeedController:
    def __init__(self, max_speed=18, hard_turn_breaking_speed=0, medium_multiplier=0.8, slow_turn_multiplier=0.4):
        self.max_speed = max_speed
        self.hard_turn_breaking_speed = hard_turn_breaking_speed
        self.medium_multiplier = medium_multiplier
        self.slow_turn_multiplier = slow_turn_multiplier
        self.__current_speed = [self.get_max_speed(), self.get_max_speed()]

    def get_current_speed_left(self):
        return self.__current_speed[0]

    def get_current_speed_right(self):
        return self.__current_speed[1]

    def set_speed(self, left=0, right=0):
        #print(left,right)
        self.set_speed_left(left)
        self.set_speed_right(right)

    def set_speed_left(self, speed):
        self.__current_speed[0] = speed
        motorL(speed)

    def set_speed_right(self, speed):
        self.__current_speed[1] = speed
        motorR(speed)

    def get_hard_turn_breaking_speed(self):
        return self.hard_turn_breaking_speed

    def get_max_speed(self):
        return self.max_speed

    def get_hard_turn_braking_speed(self):
        return self.hard_turn_breaking_speed

    def get_medium_speed(self):
        return self.max_speed * self.medium_multiplier

    def get_slow_turn_speed(self):
        return self.max_speed * self.slow_turn_multiplier
