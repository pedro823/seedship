import time

class GameStats:

    def __init__(self):
        self.timer_start = time.time()
        self.time_elapsed = None
        self.planets_scanned = 0
        self.planets_probed = 0
        self.total_damage_taken = 0
        self.sleeps_taken = 0
        self.modules_upgraded = 0

    def end_game():
        time_end = time.time()
        self.time_elapsed = time_end - self.timer_start

    def get_elapsed_time() -> str:
        if self.time_elapsed is None:
            return ""
        m, s = divmod(end - self.timer_start, 60)
        h, m = divmod(m, 60)
        return '%02d:%02d:%02d'.format(h, m, s)