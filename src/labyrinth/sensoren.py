debug = False

import board
import time
from analogio import AnalogIn

analog_Pin1 = AnalogIn(board.A0)
analog_Pin2 = AnalogIn(board.A1)
analog_Pin3 = AnalogIn(board.A2)
analog_Pin4 = AnalogIn(board.A3)
analog_Pin5 = AnalogIn(board.A4)

threshold_white = 200


def is_white(analog_value):
    return analog_value > threshold_white


def sensor_a2d(analogWert):
    return 0 if is_white(analogWert) else 1


def query_sensor():
    sensor_value1 = round(analog_Pin1.value / 100)
    sensor_value2 = round(analog_Pin2.value / 100)
    sensor_value3 = round(analog_Pin3.value / 100)
    sensor_value4 = round(analog_Pin4.value / 100)
    sensor_value5 = round(analog_Pin5.value / 100)

    sensor_value1d = sensor_a2d(sensor_value1)
    sensor_value2d = sensor_a2d(sensor_value2)
    sensor_value3d = sensor_a2d(sensor_value3)
    sensor_value4d = sensor_a2d(sensor_value4)
    sensor_value5d = sensor_a2d(sensor_value5)

    sensor_values = [sensor_value1d, sensor_value2d, sensor_value3d, sensor_value4d, sensor_value5d]

    if debug:
        print(sensor_value1d, sensor_value2d, sensor_value3d, sensor_value4d, sensor_value5d)

    return sensor_values
