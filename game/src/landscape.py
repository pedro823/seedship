from .util import Color
from .language import TXT


def translate_landscape(type, quality):
    return TXT['landscape'][type][quality]


class AvailableLandscape:
    class Plants:
        class Unicelular:
            text = translate_landscape('plants', 'unicelular')
            color = Color.YELLOW

        class Venomous:
            text = translate_landscape('plants', 'venomous')
            color = Color.RED

        class Edible:
            text = translate_landscape('plants', 'edible')
            color = Color.GREEN

        all_possible = [Unicelular, Venomous, Edible]

    class Animals:
        class Unicelular:
            text = translate_landscape('animals', 'unicelular')
            color = Color.YELLOW

        class Dangerous:
            text = translate_landscape('animals', 'dangerous')
            color = Color.RED

        class Tameable:
            text = translate_landscape('animals', 'tameable')
            color = Color.GREEN

        all_possible = [Unicelular, Dangerous, Tameable]

    class Terrain:
        class Dangerous:
            text = translate_landscape('terrain', 'dangerous')
            color = Color.RED

        class Beautiful:
            text = translate_landscape('terrain', 'beautiful')
            color = Color.GREEN

        class Habitable:
            text = translate_landscape('terrain', 'habitable')
            color = Color.GREEN

        all_possible = [Dangerous, Beautiful, Habitable]

    class Monuments:
        class Abandoned:
            text = translate_landscape('monuments', 'abandoned')
            color = Color.LIGHT_GREEN

        class UnknownMinerals:
            text = translate_landscape('monuments', 'unknown_minerals')
            color = Color.GREEN

        all_possible = [Abandoned, UnknownMinerals]

    class Satellites:
        class ResourceRich:
            text = translate_landscape('satellites', 'resource_rich')
            color = Color.GREEN

        class Resourceful:
            text = translate_landscape('satellites', 'resourceful')
            color = Color.LIGHT_GREEN

        all_possible = [ResourceRich, Resourceful]
