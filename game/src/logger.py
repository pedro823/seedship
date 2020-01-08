from .planet import Planet
from .seedship import Seedship
from datetime import datetime
import os
import json


def get_current_datetime():
    return datetime.now()\
                   .isoformat()\
                   .split('.')[0]\
                   .replace('-', '_')

def create_log_folder(f):
    def _f(*args, **kwargs):
        os.makedirs("log", exist_ok=True)
        f(*args, **kwargs)
    return _f

class Logger:

    log_file = f'log/seedship_{get_current_datetime()}.txt'
    planet_count = 0

    @classmethod
    @create_log_folder
    def log_planet(cls, planet: Planet):
        ''' Logs a visit onto a planet '''
        cls.planet_count += 1
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_found_planet {cls.planet_count} '
                    + f'-> {json.dumps(planet.to_dict())}\n')

    @classmethod
    @create_log_folder
    def log_damage(cls, seedship: Seedship, damage: dict):
        ''' Logs damage taken '''
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_took_damage {json.dumps(damage)} {json.dumps(seedship.to_dict())}\n')

    @classmethod
    @create_log_folder
    def log_probe(cls, probes_left: int):
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_probed {probes_left}\n')

    @classmethod
    @create_log_folder
    def log_waste(cls, seedship: Seedship, waste: dict):
        ''' Logs waste of consumable '''
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_wasted {json.dumps(waste)} {json.dumps(seedship.to_dict())}\n')

    @classmethod
    @create_log_folder
    def log_seed(cls, seed: int):
        ''' Logs seed of RNG used in the game '''
        with open(cls.log_file, mode='a') as f:
            f.write(f'RNG seed = {seed}')

if __name__ == '__main__':
    s = Seedship()
    s.find_new_planet()
    Logger.log_planet(s.planet)
    Logger.log_damage(s, {})
