from src.util import Color
from src.language import TXT


def translate_feature(scanner_type: str, quality: str) -> str:
    return TXT['scanner']['hits'][scanner_type][quality]


class AvailableFeatures:
    class Atmosphere:
        class Corrosive:
            text = translate_feature('atmosphere', 'corrosive')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [10, 5, 0]  # 0, 1, 2

        class NoAtmosphere:
            text = translate_feature('atmosphere', 'none')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 10, 0]  # 0, 1, 2

        class Rare:
            text = translate_feature('atmosphere', 'rare')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.9,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 10, 5]  # 0, 1, 2

        class SemiRare:
            text = translate_feature('atmosphere', 'semi_rare')
            color = Color.LIGHT_GREEN
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 1.0
            }
            probability = [15, 25, 30]  # 0, 1, 2

        class Good:
            text = translate_feature('atmosphere', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.2,
                'animals': 1.2,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 40, 60]  # 0, 1, 2

        class Unbreathable:
            text = translate_feature('atmosphere', 'unbreathable')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.8,
                'animals': 0.1,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [15, 10, 5]  # 0, 1, 2

        all_possible = [Corrosive,
                        NoAtmosphere,
                        Rare,
                        SemiRare,
                        Good,
                        Unbreathable]

    class Temperature:
        class VeryLow:
            text = translate_feature('temperature', 'very_low')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.3,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.1,
                'satellites': 1.0
            }
            probability = [20, 5, 0]  # 0, 1, 2

        class Low:
            text = translate_feature('temperature', 'low')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.5,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 20, 15]  # 0, 1, 2

        class Good:
            text = translate_feature('temperature', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.2,
                'animals': 1.2,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 45, 70]  # 0, 1, 2

        class High:
            text = translate_feature('temperature', 'high')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 20, 15]  # 0, 1, 2

        class VeryHigh:
            text = translate_feature('temperature', 'very_high')
            color = Color.RED
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 10, 0]  # 0, 1, 2

        all_possible = [VeryLow, Low, Good, High, VeryHigh]

    class Water:
        class NoWater:
            text = translate_feature('water', 'none')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 0.7,
                'monuments': 0.3,
                'satellites': 1.0
            }
            probability = [20, 5, 0]  # 0, 1, 2

        class Trace:
            text = translate_feature('water', 'trace')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.6,
                'animals': 0.4,
                'terrain': 1.0,
                'monuments': 0.6,
                'satellites': 1.0
            }
            probability = [20, 15, 5]  # 0, 1, 2

        class Scarce:
            text = translate_feature('water', 'scarce')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 20, 10]  # 0, 1, 2

        class Good:
            text = translate_feature('water', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.1,
                'animals': 1.1,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 45, 75]  # 0, 1, 2

        class PlanetWideOcean:
            text = translate_feature('water', 'planet_wide_ocean')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 0.1,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        all_possible = [NoWater, Trace, Scarce, Good, PlanetWideOcean]

    class Gravity:
        class VeryLow:
            text = translate_feature('gravity', 'very_low')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 0.7,
                'monuments': 0.3,
                'satellites': 0.0
            }
            probability = [20, 5, 0]  # 0, 1, 2

        class Low:
            text = translate_feature('gravity', 'low')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.8,
                'animals': 0.8,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 0.3
            }
            probability = [20, 25, 15]  # 0, 1, 2

        class Good:
            text = translate_feature('gravity', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.1,
                'animals': 1.1,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 0.7
            }
            probability = [20, 40, 70]  # 0, 1, 2

        class High:
            text = translate_feature('gravity', 'high')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.8,
                'animals': 0.8,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 1.1
            }
            probability = [20, 25, 15]  # 0, 1, 2

        class VeryHigh:
            text = translate_feature('gravity', 'very_high')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.5,
                'animals': 0.2,
                'terrain': 0.7,
                'monuments': 0.3,
                'satellites': 1.4
            }
            probability = [20, 5, 0]  # 0, 1, 2

        all_possible = [VeryLow, Low, Good, High, VeryHigh]

    class Resources:
        class NoResource:
            text = translate_feature('resources', 'none')
            color = Color.RED
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 0.1,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [25, 0, 0]  # 0, 1, 2

        class Scarce:
            text = translate_feature('resources', 'scarce')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.3,
                'satellites': 1.0
            }
            probability = [25, 30, 5]  # 0, 1, 2

        class LightlyScarce:
            text = translate_feature('resources', 'lightly_scarce')
            color = Color.LIGHT_GREEN
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 0.1,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [25, 30, 40]  # 0, 1, 2

        class Good:
            text = translate_feature('resources', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [25, 35, 55]  # 0, 1, 2

        all_possible = [NoResource, Scarce, LightlyScarce, Good]

    all_hits = [Atmosphere, Temperature]
