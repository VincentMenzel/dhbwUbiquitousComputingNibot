
#
# Sensorenabfrage - Robo - Test 1
# Board: Metro M4 Express
# Sensoren: Waveshare Tracker Sensor (5x Analog)
# 05.07.21 - wb
# v0.2
#

import board
import time
from analogio import AnalogIn

analog_Pin1 = AnalogIn(board.A0)
analog_Pin2 = AnalogIn(board.A1)
analog_Pin3 = AnalogIn(board.A2)
analog_Pin4 = AnalogIn(board.A3)
analog_Pin5 = AnalogIn(board.A4)

def is_white(analogWert):
    grenzwert_Weiss = 300
    return analogWert > grenzwert_Weiss

def sensor_ADchange(analogWert):
    return is_white(analogWert) if 0 else 1


def sensorAbfrage():

    SensorDaten1 = round(analog_Pin1.value / 100)
    SensorDaten2 = round(analog_Pin2.value / 100)
    SensorDaten3 = round(analog_Pin3.value / 100)
    SensorDaten4 = round(analog_Pin4.value / 100)
    SensorDaten5 = round(analog_Pin5.value / 100)

    sensorWert_1D = sensor_ADchange(SensorDaten1)
    sensorWert_2D = sensor_ADchange(SensorDaten2)
    sensorWert_3D = sensor_ADchange(SensorDaten3)
    sensorWert_4D = sensor_ADchange(SensorDaten4)
    sensorWert_5D = sensor_ADchange(SensorDaten5)

    sensorWerte = [sensorWert_1D, sensorWert_2D, sensorWert_3D, sensorWert_4D, sensorWert_5D]

    return sensorWerte