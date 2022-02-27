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


# Ensures that the amount passed in is within the valid boundries of the speed.
def get_valid_speed(amount):
    if amount >= 0 and amount <= 100:
        return int(amount)
    elif amount < 0:
        return 0
    elif amount > 100:
        return 100


def motorL(target_speed):  # linker Motor (Geschwindigkeit [0-100])
    speed = get_valid_speed(target_speed)
    if speed < 0:
        MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = -speed * 650  # zwischen 0 und 65535
    elif speed > 0:
        MotorL_In1.duty_cycle = speed * 650  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = 0  # zwischen 0 und 65535
    else:
        MotorL_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorLB_In1.duty_cycle = 0  # zwischen 0 und 65535

    # mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    # MotorL_In1.duty_cycle = mSpeed


def motorR(target_speed):  # rechter Motor (Geschwindigkeit [0-100])
    speed = get_valid_speed(target_speed)
    if speed < 0:
        MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = -speed * 650  # zwischen 0 und 65535
    elif speed > 0:
        MotorR_In1.duty_cycle = speed * 650  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = 0  # zwischen 0 und 65535
    else:
        MotorR_In1.duty_cycle = 0  # zwischen 0 und 65535
        MotorRB_In1.duty_cycle = 0  # zwischen 0 und 65535

    # mSpeed = speed * 650  # es werden Werte von 0-65535 benoetigt
    # MotorR_In1.duty_cycle = mSpeed
