from language import LANG_DICT
import random as r
from features import AvailableFeatures
from landscape import AvailableLandscape


def translate(attribute: str) -> str:
    ''' Does one-time translation of every planet feature. '''
    return LANG_DICT['scanner']['categories'].get(attribute, attribute)


class Planet:

    ATTRIBUTES = dict((attribute, translate(attribute))
                      for attribute in ['atmosphere',
                                        'gravity',
                                        'temperature',
                                        'water',
                                        'resources'])

    ATMOSPHERE_POSSIBILITIES = AvailableFeatures.Atmosphere.all_possible
    TEMPERATURE_POSSIBILITIES = AvailableFeatures.Temperature.all_possible
    GRAVITY_POSSIBILITIES = AvailableFeatures.Gravity.all_possible
    WATER_POSSIBILITIES = AvailableFeatures.Water.all_possible
    RESOURCES_POSSIBILITIES = AvailableFeatures.Resources.all_possible

    possibility_map = {
        'atmosphere': ATMOSPHERE_POSSIBILITIES,
        'temperature': TEMPERATURE_POSSIBILITIES,
        'gravity': GRAVITY_POSSIBILITIES,
        'water': WATER_POSSIBILITIES,
        'resources': RESOURCES_POSSIBILITIES
    }

    landscape_map = {
        'plants': AvailableLandscape.Plants.all_possible,
        'animals': AvailableLandscape.Animals.all_possible,
        'terrain': AvailableLandscape.Terrain.all_possible,
        'monuments': AvailableLandscape.Monuments.all_possible,
        'satellites': AvailableLandscape.Satellites.all_possible
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
        multipliers = {
            'plants': 0.25,
            'animals': 0.25,
            'terrain': 0.25,
            'monuments': 0.25,
            'satellites': 0.25
        }
        landscapes = []
        for feature in [self.atmosphere,
                        self.gravity,
                        self.temperature,
                        self.water,
                        self.resources]:
            for name in multipliers:
                multipliers[name] *= feature.feature_multiplier[name]
        for name, treshold in multipliers.items():
            if r.random() < treshold:
                landscapes.append(r.choice(self.landscape_map[name]))
        return landscapes
