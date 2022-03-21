import time

from util.timing import get_time_diff_in_sec


class TimingController:

    def __init__(self):
        self.__set_time_to_now()

    def reset_timer(self):
        self.__set_time_to_now()

    def __set_time_to_now(self):
        self.__timer_started_at = time.time()

    def get_timer_started_at(self):
        return self.__timer_started_at

    def time_since_timestamp(self, timestamp: float):
        return get_time_diff_in_sec(self.__timer_started_at, timestamp)

    def seconds_since_start(self):
        return self.time_since_timestamp(time.time())

