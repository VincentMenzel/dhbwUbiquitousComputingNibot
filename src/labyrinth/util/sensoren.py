import board
import time
from analogio import AnalogIn

threshold_white = 200

board_inputs = [board.A0, board.A1, board.A2, board.A3, board.A4]
pins = [AnalogIn(v) for v in board_inputs]

def is_white(analog_value):
    return analog_value > threshold_white

def sensor_a2d(analogWert):
    return 0 if is_white(analogWert) else 1

def query_sensor(debug = False):
    sensor_values_analog = [round(analog.value / 100) for analog in pins]
    sensor_values_digital = [sensor_a2d(value) for value in sensor_values_analog]

    if debug:
        print(sensor_values_digital)

    return sensor_values_digital
