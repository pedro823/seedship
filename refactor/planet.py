from language import LANG_DICT
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

    ATMOSPHERE_POSSIBILITIES = settings.AvailableHits.Atmosphere.all_possible
    TEMPERATURE_POSSIBILITIES = settings.AvailableHits.Temperature.all_possible
    GRAVITY_POSSIBILITIES = settings.AvailableHits.Gravity.all_possible
    WATER_POSSIBILITIES = settings.AvailableHits.Water.all_possible
    RESOURCES_POSSIBILITIES = settings.AvailableHits.Resources.all_possible

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
        upgrade_level = scanner.upgrade_level

        pass


    def __init__(self, atmosphere, gravity, temperature, water, resources):
        self.atmosphere = atmosphere
        self.gravity = gravity
        self.temperature = temperature
        self.water = water
        self.resources = resources
