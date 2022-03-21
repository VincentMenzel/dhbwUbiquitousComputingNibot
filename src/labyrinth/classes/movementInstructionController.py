from sensorController import SensorController


class MovementInstructionController:
    def __init__(self, sensor_data: SensorController):
        self.forward = True
        self.left = False
        self.medium_left = False
        self.hard_left = False
        self.right = False
        self.medium_right = False
        self.hard_right = False
        self.__sensor_data = sensor_data

    def should_drive_right(self):
        return bool(
            self.__sensor_data.get_sensor_value_r() and not self.__sensor_data.get_sensor_value_rr() and not self.__sensor_data.get_sensor_value_l())

    def should_drive_hard_right(self):
        return bool(self.__sensor_data.get_sensor_value_rr() and not self.__sensor_data.get_sensor_value_r())

    def should_drive_medium_right(self):
        return bool(
            self.__sensor_data.get_sensor_value_r()
            and self.__sensor_data.get_sensor_value_rr()
            and not self.__sensor_data.get_sensor_value_l()
            and not self.__sensor_data.get_sensor_value_ll()
        )

    def should_drive_left(self):
        return bool(
            self.__sensor_data.get_sensor_value_l()
            and not self.__sensor_data.get_sensor_value_ll()
            and not self.__sensor_data.get_sensor_value_r()
        )

    def should_drive_hard_left(self):
        return bool(
            self.__sensor_data.get_sensor_value_ll()
            and not self.__sensor_data.get_sensor_value_l()
            or self.__sensor_data.get_sensor_value_ll()
            and self.__sensor_data.get_sensor_value_l()
            and self.__sensor_data.get_sensor_value_m()
        )

    def should_drive_medium_left(self):
        return bool(
            self.__sensor_data.get_sensor_value_l()
            and self.__sensor_data.get_sensor_value_ll()
            and not self.__sensor_data.get_sensor_value_m()
            and not self.__sensor_data.get_sensor_value_r()
            and not self.__sensor_data.get_sensor_value_rr()
        )

    def should_drive_forward(self):
        middle_black = \
            self.__sensor_data.get_sensor_value_m() \
            and not self.__sensor_data.get_sensor_value_l() \
            and not self.__sensor_data.get_sensor_value_ll() \
            and not self.__sensor_data.get_sensor_value_r() \
            and not self.__sensor_data.get_sensor_value_rr()

        middle_three_black = \
            self.__sensor_data.get_sensor_value_m() \
            and self.__sensor_data.get_sensor_value_l() \
            and not self.__sensor_data.get_sensor_value_ll() \
            and self.__sensor_data.get_sensor_value_r() \
            and not self.__sensor_data.get_sensor_value_rr()

        return bool(middle_black or middle_three_black)

    def update(self, sensor_data: SensorController):
        self.__sensor_data = sensor_data

        self.forward = self.should_drive_forward()
        self.left = self.should_drive_left()
        self.medium_left = self.should_drive_medium_left()
        self.hard_left = self.should_drive_hard_left()
        self.right = self.should_drive_right()
        self.medium_right = self.should_drive_medium_right()
        self.hard_right = self.should_drive_hard_right()