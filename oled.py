import board
import adafruit_ssd1306
import busio as io

width = 128
height = 64

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=0x3c)

def show_default():
    clear_display()
    oled.text('Hello World!',0,0,1)
    update_display()

def update_display():
    oled.show()

def clear_display():
    oled.fill(0)

def print_movement_instrcution(direction):
    oled.text(direction, 0, 0, 1)

def print_motor_speed(speed_r, speed_l):
    oled.text('Speed L: %s' % (speed_l), 10, 0, 1)
    oled.text('Speed R: %s' % (speed_r), 20, 0, 1)