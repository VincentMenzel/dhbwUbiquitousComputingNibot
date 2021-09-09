import board
import adafruit_ssd1306
import busio as io
import time


width = 128
height = 64

i2c = io.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=0x3c)

rick_roll = "We're no strangers to love You know the rules and so do I A full commitment's what I'm thinking of You wouldn't get this from any other guy I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you We've known each other for so long Your heart's been aching but you're too shy to say it Inside we both know what's been going on We know the game and we're gonna play it And if you ask me how I'm feeling Don't tell me you're too blind to see Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give, never gonna give (Give you up) We've known each other for so long Your heart's been aching but you're too shy to say it Inside we both know what's been going on We know the game and we're gonna play it I just wanna tell you how I'm feeling Gotta make you understand Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye Never gonna tell a lie and hurt you Never gonna give you up Never gonna let you down Never gonna run around and desert you Never gonna make you cry Never gonna say goodbye".split(" ")

word = 0
last_updated_rick_at = 0


def show_default():
    clear_display()
    oled.text('Hello World!',0,0,1)
    update_display()

def update_display():
    update_rick()
    oled.show()

def clear_display():
    oled.fill(0)

def print_countdown(countdown_text, offset):
    clear_display()

    for i in range(width - offset):
        oled.pixel(i, offset, 1)
        oled.pixel(i, height - 1 - offset, 1)


    for i in range(height - offset):
        oled.pixel(offset, i, 1)
        oled.pixel(width - 1 - offset, i, 1)

    print_height = height / 2 - 5

    if type(countdown_text) == str:
        oled.text(countdown_text, width/2-(len(countdown_text)*4))
    else:
        oled.text(countdown_text, width / 2, print_height)

    update_display()

def print_movement_instrcution(direction):
    oled.text(direction, 0, 0, 1)

def print_motor_speed(speed_r, speed_l):
    oled.text('Speed L: %s' % (speed_l), 0, 10, 1)
    oled.text('Speed R: %s' % (speed_r), 0, 20, 1)

def update_rick():
    global last_updated_rick_at
    global word

    oled.text("Playing: 'Rick Roll'", 0,40,1)
    oled.text(" ".join(rick_roll[word % len(rick_roll):word+3 % len(rick_roll)]), 0, 40, 1)

    if int(time.time() - last_updated_rick_at >= 2):
        last_updated_rick_at = int(time.time())
        word += 3