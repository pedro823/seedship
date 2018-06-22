from random import SystemRandom as random
r = random()
import os
import time
import datetime
from logger import Logger
from settings import *

def print_noln(*args, **kwargs):
    print(*args, **kwargs, end='', flush=True)

class Scanner:

    def __init__(self):
        log_file = 'log/sdshp_' + datetime.datetime.now().isoformat()
        self.logger = Logger(self, outfile=log_file)
        self.probes = 10
        self.planet_list = []
        self.scanner_status = {
            'atmosfera': 100,
            'gravidade': 100,
            'temperatura': 100,
            'água': 100,
            'recursos': 100
        }
        self.scanner_levels = {
            'atmosfera': 0,
            'gravidade': 0,
            'temperatura': 0,
            'água': 0,
            'recursos': 0
        }
        self.planet_rng = {
            'atmosfera': [],
            'gravidade': [],
            'temperatura': [],
            'água': [],
            'recursos': []
        }
        self.scan_settings = SCAN_SETTINGS
        self.available_options = AVAIL_OPTIONS
        # build matrix
        for key in self.planet_rng:
            for i in range(3):
                self.planet_rng[key].append([])
        # build level 0, level 1 and level 2 scanners
        try:
            for scanner_type, scanner_list in self.planet_rng.items():
                specific_scanner_settings = self.scan_settings[scanner_type]
                for i in range(3):
                    j = 0
                    for k in range(100):
                        j += specific_scanner_settings[i].count(k)
                        self.planet_rng[scanner_type][i].append(self.available_options[scanner_type][j])
        except Exception as ex:
            raise BadConfig(str(ex))

    def print_status(self):
        for key, value in self.scanner_status.items():
            if value < 40:
                color = Color.LIGHT_RED
            elif value < 70:
                color = Color.YELLOW
            elif value < 95:
                color = Color.LIGHT_GREEN
            else:
                color = Color.GREEN
            str_left = Color.RESET + key.capitalize() + ': '
            str_right = color + str(value) + '% ' + Color.RESET

            string = str_left.ljust(17) + str_right.ljust(18) + '(' + str(self.scanner_levels[key]) + ')'
            print(string)
            time.sleep(0.2)
        print('Sondas restantes: %s' % self.probes)

    def damage_status(self, key, amount):
        if self.scanner_status.get(key) is None:
            raise Exception(key + ' não é um scanner')
        amount = int(amount) # Auto raises error
        self.scanner_status[key] = max(self.scanner_status[key] - amount, 0)

    def upgrade_scanner(self, key):
        if self.scanner_levels.get(key) is None:
            raise Exception(key + ' não é um scanner')
        if self.scanner_levels[key] >= 2:
            raise Exception(key + ' está no upgrade máximo')
        self.scanner_levels[key] += 1

    def generate_hits(self):
        random_hits = dict(
                          (key, True if r.randint(0, 99) < self.scanner_status[key] else False)
                          for key in self.scanner_status
                          )
        return random_hits

    def generate_planet(self, bonus=True):
        random_planet = dict(
                          (key, self.planet_rng[key][self.scanner_levels[key] if bonus else 0][r.randint(0, 99)])
                          for key in self.scanner_status
                          )
        self.logger.log('generated planet', random_planet, 'with self.scanner_levels =', self.scanner_levels)
        self.planet_list.append(random_planet)
        return random_planet

    def print_planet(self, planet, hits, probe=False, features=None):
        for key, value in planet.items():
            string = Color.WHITE + key.capitalize()
            print_noln(string)
            for i in range(3):
                time.sleep(0.3)
                print_noln('.')

            if hits.get(key) or probe:
                result = value[1] + value[0] + Color.RESET
            else:
                result = SCAN_FAILURE
            time.sleep(0.5)
            print(' ' + result)
            time.sleep(1)
        if probe and features:
            for feature in features:
                time.sleep(0.7)
                print(feature[1] + feature[0] + Color.RESET)

    def generate_planet_features(self, planet):
        # Calculates chances based on settings
        if self.probes:
            matrix_features = [value[2:] for value in planet.values()]
            chances = []
            for idx, chance in enumerate(PROBE_HIT_CHANCE):
                for line in matrix_features:
                    chance *= line[idx]
                chances.append(chance)

            features = []
            # Rolls to see if it hits
            for idx, feature_chance in enumerate(PROBE_FEATURES):
                if r.random() < chances[idx]:
                    # Success, adds sample to features
                    features.append(r.sample(feature_chance, 1)[0])
            # self.logger.log('planet', planet, 'generated features', features)
            self.probes -= 1
            return features
        else:
            raise Exception('Acabaram as sondas!')

if __name__ == '__main__':
    a = Scanner()
    # a.damage_status('atmosfera', 35)
    # a.damage_status('água', 200)
    # a.damage_status('recursos', 10)
    # a.damage_status('gravidade', 80)
    # for i in range(2):
    #     a.upgrade_scanner('atmosfera')
    #     a.upgrade_scanner('água')
    #     a.upgrade_scanner('gravidade')
    #     a.upgrade_scanner('recursos')
    #     a.upgrade_scanner('temperatura')
    a.print_status()
    for i in range(10):
        a.print_planet(a.generate_planet(), a.generate_hits(), True)
