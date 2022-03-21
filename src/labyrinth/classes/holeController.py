from classes.timingController import TimingController

PHASE_1 = 0
PHASE_2 = 1
PHASE_3 = 2
PHASE_4 = 3
PHASE_5 = 4


class HoleController(TimingController):
    __phase_durations = [2,1,1]

    def __init__(self):
        super().__init__()
        self.__phase = PHASE_1
        self.__lost_sight_of_line = False

    def set_phase(self, phase: PHASE_2 or PHASE_3 or PHASE_4 or PHASE_5):
        self.__phase = phase
        self.reset_timer()

    def get_phase(self) -> int:
        return self.__phase

    def is_phase(self, phase: PHASE_1 or PHASE_2 or PHASE_3 or PHASE_4 or PHASE_5):
        return self.__phase == phase

    def set_lost_sight(self):
        self.__lost_sight_of_line = True

    def has_lost_sight(self):
        return self.__lost_sight_of_line

    def is_phase_complete(self):
        if self.is_phase(PHASE_1):
            return self.seconds_since_start() > HoleController.__phase_durations[0]
        elif self.is_phase(PHASE_2):
            return self.seconds_since_start() > HoleController.__phase_durations[1]
        elif self.is_phase(PHASE_3):
            return self.seconds_since_start() > HoleController.__phase_durations[2]
