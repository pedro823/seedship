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
        self.total_fuel_wasted = 0

    def end_game(self):
        time_end = time.time()
        self.time_elapsed = time_end - self.timer_start

    def get_elapsed_time(self) -> str:
        if self.time_elapsed is None:
            self.end_game()
        m, s = divmod(self.time_elapsed, 60)
        h, m = divmod(m, 60)
        return '%02d:%02d:%02d' % (h, m, s)

    def get_stats(self) -> dict:
        return {
            'time_elapsed': self.get_elapsed_time(),
            'planets_scanned': self.planets_scanned,
            'planets_probed': self.planets_probed,
            'total_damage_taken': self.total_damage_taken,
            'sleeps_taken': self.sleeps_taken,
            'modules_upgraded': self.modules_upgraded,
            'total_fuel_wasted': self.total_fuel_wasted
        }