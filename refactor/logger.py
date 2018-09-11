from planet import Planet
from seedship import Seedship
from datetime import datetime
import json


def get_current_datetime():
    return datetime.now()\
                   .isoformat()\
                   .split('.')[0]\
                   .replace('-', '_')


class Logger:

    log_file = f'log/seedship_{get_current_datetime()}.txt'
    planet_count = 0

    @classmethod
    def log_planet(cls, planet: Planet):
        ''' Logs a visit onto a planet '''
        cls.planet_count += 1
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_found_planet {cls.planet_count} '
                    + f'-> {json.dumps(planet.to_dict())}\n')

    @classmethod
    def log_damage(cls, seedship: Seedship, damage: dict):
        ''' Logs damage taken '''
        with open(cls.log_file, mode='a') as f:
            f.write(f'seedship_took_damage {json.dumps(damage)}')


if __name__ == '__main__':
    s = Seedship()
    s.find_new_planet()
    Logger.log_planet(s.planet)
