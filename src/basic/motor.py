#
# Motoransteuerung - Robo - Test 1
# Board: Metro M4 Express
# Adafruit DRV8871 Brushed DC Motor Driver
# 18.06.21 - wb
# v0.2
#

import board
import pulseio

MotorR_In1 = pulseio.PWMOut(board.D10)
MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535

MotorRB_In1 = pulseio.PWMOut(board.D11)
MotorRB_In1.duty_cycle = 0  # zwischen 0 und 65535

MotorL_In1 = pulseio.PWMOut(board.D9)
MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535

MotorLB_In1 = pulseio.PWMOut(board.D8)
MotorLB_In1.duty_cycle = 0  # zwischen 0 und 65535

def motorL(speed):  # linker Motor (Geschwindigkeit [0-100])
    if speed < 0:
        MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = -speed * 650  # zwischen 0 und 65535
    elif speed > 0:
        MotorL_In1.duty_cycle = speed * 650  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = 0  # zwischen 0 und 65535    
    else:
        MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = 0  # zwischen 0 und 65535    

    #mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    #MotorL_In1.duty_cycle = mSpeed

def motorR(speed):  # rechter Motor (Geschwindigkeit [0-100])
    if speed < 0:
        MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = -speed * 650  # zwischen 0 und 65535
    elif speed > 0:
        MotorR_In1.duty_cycle = speed * 650  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = 0  # zwischen 0 und 65535    
    else:
        MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = 0  # zwischen 0 und 65535    
    
    #mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    #MotorR_In1.duty_cycle = mSpeed
