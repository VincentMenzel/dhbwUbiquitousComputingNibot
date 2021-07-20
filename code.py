#
# Liniensensor - Robo - Test 1
# Adafruit CircuitPython 6.2.0
# Board: Metro M4 Express
# Sensoren: Waveshare Tracker Sensor (5x Analog)
# 05.07.21 - wb
# v0.2
#

import time
from motor import *
from sensoren import *

maxSpeed = 25  # maximale Geschwindigkeit (0-100)

while True:

    sensorWerte = sensorAbfrage()  # Liste der Sensorwerte holen (0 = weiß, 1 = schwarz)
    sensorWert_R = sensorWerte[3]  # rechter Sensor
    sensorWert_M = sensorWerte[2]  # mittlerer Sensor
    sensorWert_L = sensorWerte[1]  # linker Sensor

    #print(sensorWert_L, sensorWert_M, sensorWert_R)
    #time.sleep(0.25)

    # Fahrtrichtung festlegen
    if sensorWert_M == 1:
        #print("driveForward")
        motorR(maxSpeed)
        motorL(maxSpeed)

    if sensorWert_L == 1:
        #print("driveLeft")
        motorR(maxSpeed)
        motorL(0)

    if sensorWert_R == 1:
        #print("driveRight")
        motorR(0)
        motorL(maxSpeed)



