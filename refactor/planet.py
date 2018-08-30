from language import LANG_DICT
import random as r
import settings


def __translate(attribute: str) -> str:
    ''' Does one-time translation of every planet feature. '''
    return LANG_DICT['scanner']['categories'].get(attribute, attribute)


class Planet:

    ATTRIBUTES = dict((attribute, __translate(attribute))
                      for attribute in ['atmosphere',
                                        'gravity',
                                        'temperature',
                                        'water',
                                        'resources'])

    ATMOSPHERE_POSSIBILITIES = settings.AvailableFeatures.Atmosphere.all_possible
    TEMPERATURE_POSSIBILITIES = settings.AvailableFeatures.Temperature.all_possible
    GRAVITY_POSSIBILITIES = settings.AvailableFeatures.Gravity.all_possible
    WATER_POSSIBILITIES = settings.AvailableFeatures.Water.all_possible
    RESOURCES_POSSIBILITIES = settings.AvailableFeatures.Resources.all_possible

    possibility_map = {
        'atmosphere': ATMOSPHERE_POSSIBILITIES,
        'temperature': TEMPERATURE_POSSIBILITIES,
        'gravity': GRAVITY_POSSIBILITIES,
        'water': WATER_POSSIBILITIES,
        'resources': RESOURCES_POSSIBILITIES
    }

    @classmethod
    def from_scanners(cls, scanners: list):
        planet_features = {}
        for scanner_name, scanner in scanners.items():
            planet_features[scanner_name] = cls.generate_feature(
                scanner,
                cls.possibility_map[scanner_name]
            )
        return Planet(**planet_features)

    @classmethod
    def generate_feature(cls, scanner, possibilities):
        ''' Generates a random number and matches it with a planet's feature '''
        upgrade_level = scanner.upgrade_level
        random_number = r.randint(1, 100)
        current_sum = 0
        for feature in possibilities:
            if random_number <= current_sum + feature.probability[upgrade_level]:
                return feature
            current_sum += feature.probability[upgrade_level]
        raise Exception(f'Unexpected branch. random_number={random_number}'
                        + f'current_sum={current_sum} possibilities={possibilities}')

    def __init__(self, atmosphere, gravity, temperature, water, resources):
        self.atmosphere = atmosphere
        self.gravity = gravity
        self.temperature = temperature
        self.water = water
        self.resources = resources
        self.landscape = self.generate_landscape()

    def generate_landscape(self):
        
