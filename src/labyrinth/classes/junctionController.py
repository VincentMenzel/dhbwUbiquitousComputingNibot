from classes.timingController import TimingController


class JunctionController(TimingController):
    def __init__(self):
        super().__init__()
        self.__junction_attempt_lost_black = False

    def get_junction_attempt_lost_black(self):
        return self.__junction_attempt_lost_black

    def set_junction_attempt_lost_black(self):
        self.__junction_attempt_lost_black = True
