import sys
sys.path.insert(0,'/classes')
from classes.nibot import NiBot


def main():
    robot = NiBot(debug= False, print_speed= False)
    robot.play_start_countdown()

    while True:
        robot.run()

main()
