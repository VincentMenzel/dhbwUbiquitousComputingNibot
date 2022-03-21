class SensorController:
    def __init__(self):
        self.__sensor_values = [0, 0, 0, 0, 0]

    def get_sensor_values(self):
        return self.__sensor_values

    def set_sensor_values(self, sensor_values):
        self.__sensor_values = sensor_values

    def get_sensor_value_rr(self):
        return self.__sensor_values[4]

    def get_sensor_value_r(self):
        return self.__sensor_values[3]

    def get_sensor_value_m(self):
        return self.__sensor_values[2]

    def get_sensor_value_l(self):
        return self.__sensor_values[1]

    def get_sensor_value_ll(self):
        return self.__sensor_values[0]

    def can_detect_black(self):
        return 1 in self.__sensor_values

    def can_detect_white(self):
        return 0 in self.__sensor_values

    def can_detect_all_except_the_middle_sensor_as_black(self):
        return bool(
            self.get_sensor_value_ll()
            and self.get_sensor_value_l()
            and not self.get_sensor_value_m()
            and self.get_sensor_value_r()
            and self.get_sensor_value_rr()
        )
    def can_detect_first_and_last_sensor_as_black_the_rest_as_white(self):
        return bool(
            self.get_sensor_value_ll()
            and not self.get_sensor_value_l()
            and not self.get_sensor_value_m()
            and not self.get_sensor_value_r()
            and self.get_sensor_value_rr()
        )

    def can_detect_three_sensors_on_the_left_as_black_the_rest_as_white(self):
        return bool(
            self.get_sensor_value_ll()
            and self.get_sensor_value_l()
            and self.get_sensor_value_m()
            and not self.get_sensor_value_r()
            and not self.get_sensor_value_rr()
        )

    def can_detect_three_sensors_on_the_right_as_black_the_rest_as_white(self):
        return bool(
            not self.get_sensor_value_ll()
            and not self.get_sensor_value_l()
            and self.get_sensor_value_m()
            and self.get_sensor_value_r()
            and self.get_sensor_value_rr()
        )

    def is_junction(self):
        return bool(
            not self.can_detect_white()
            or self.can_detect_all_except_the_middle_sensor_as_black()
            or self.can_detect_first_and_last_sensor_as_black_the_rest_as_white()
        )

    def is_half_junction_l(self):
        return bool(
            self.can_detect_three_sensors_on_the_left_as_black_the_rest_as_white()
        )

    def is_half_junction_r(self):
        return bool(
            self.can_detect_three_sensors_on_the_right_as_black_the_rest_as_white()
        )

    def is_hole(self):
        return not self.can_detect_black()

    def is_follow(self):
        return self.can_detect_black() and self.can_detect_white()
