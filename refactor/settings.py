from util import Color
from language import TXT

SCAN_HIT_PROBABILITY = {
    'Atmosfera': [
        [10, 30, 50, 65, 80], # level 0
        [5, 15, 25, 50, 90], # level 1
        [0, 0, 5, 35, 95]  # level 2
    ],
    'Temperatura': [
        [20, 40, 60, 80], # level 0
        [5, 30, 70, 95],  # level 1
        [0, 15, 85]       # level 2
    ],
    'Água': [
        [20, 40, 60, 80], # level 0
        [5, 20, 40, 85], # level 1
        [0, 5, 15, 90]  # level 2
    ],
    'Gravidade': [
        [20, 40, 60, 80], # level 0
        [5, 30, 70, 95],  # level 1
        [0, 15, 85]       # level 2
    ],
    'Recursos': [
        [25, 50, 75], # level 0
        [0, 30, 60], # level 1
        [0, 5, 40]  # level 2
    ]
}


@staticmethod
def __translate(scanner_type: str, quality: str) -> str:
    return TXT['scanner']['hits'][scanner_type][quality]


class AvailableHits:
    class Atmosphere:
        class Corrosive:
            text = __translate('atmosphere', 'corrosive')
            color = Color.RED,
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [10, 5, 0]  # 0, 1, 2

        class NoAtmosphere:
            text = __translate('atmosphere', 'none')
            color = Color.RED,
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 1.0,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 10, 0]  # 0, 1, 2

        class Rare:
            text = __translate('atmosphere', 'rare')
            color = Color.YELLOW,
            feature_multiplier = {
                'plants': 0.9,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 10, 5]  # 0, 1, 2

        class SemiRare:
            text = __translate('atmosphere', 'semi_rare')
            color = Color.LIGHT_GREEN,
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 1.0
            }
            probability = [15, 25, 30]  # 0, 1, 2

        class Good:
            text = __translate('atmosphere', 'semi_rare')
            color = Color.GREEN,
            feature_multiplier = {
                'plants': 1.2,
                'animals': 1.2,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 40, 60]  # 0, 1, 2

        class Unbreathable:
            text = __translate('atmosphere', 'unbreathable')
            color = Color.RED,
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
            text = __translate('temperature', 'very_low')
            color = Color.RED,
            feature_multiplier = {
                'plants': 0.3,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.1,
                'satellites': 1.0
            }
            probability = [20, 5, 0]  # 0, 1, 2

        class Low:
            text = __translate('temperature', 'low')
            color = Color.YELLOW,
            feature_multiplier = {
                'plants': 0.5,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 20, 15]  # 0, 1, 2

        class Good:
            text = __translate('temperature', 'good')
            color = Color.GREEN,
            feature_multiplier = {
                'plants': 1.2,
                'animals': 1.2,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 45, 70]  # 0, 1, 2

        class High:
            text = __translate('temperature', 'high')
            color = Color.YELLOW,
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 0.7,
                'satellites': 1.0
            }
            probability = [20, 20, 15]  # 0, 1, 2

        class VeryHigh:
            text = __translate('temperature', 'very_high')
            color = Color.RED,
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
            text = __translate('water', 'none')
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
            text = __translate('water', 'trace')
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
            text = __translate('water', 'scarce')
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
            text = __translate('water', 'good')
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
            text = __translate('water', 'planet_wide_ocean')
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
            text = __translate('gravity', 'very_low')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.1,
                'animals': 0.1,
                'terrain': 0.7,
                'monuments': 0.3,
                'satellites': 0.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class Low:
            text = __translate('gravity', 'low')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.8,
                'animals': 0.8,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 0.3
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class Good:
            text = __translate('gravity', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.1,
                'animals': 1.1,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 0.7
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class High:
            text = __translate('gravity', 'high')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 0.8,
                'animals': 0.8,
                'terrain': 1.0,
                'monuments': 0.9,
                'satellites': 1.1
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class VeryHigh:
            text = __translate('gravity', 'very_high')
            color = Color.RED
            feature_multiplier = {
                'plants': 0.5,
                'animals': 0.2,
                'terrain': 0.7,
                'monuments': 0.3,
                'satellites': 1.4
            }
            probability = [20, 15, 15]  # 0, 1, 2

        all_possible = [VeryLow, Low, Good, High, VeryHigh]

    class Resources:
        class NoResource:
            text = __translate('resources', 'none')
            color = Color.RED
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 0.1,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class Scarce:
            text = __translate('resources', 'scarce')
            color = Color.YELLOW
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 1.0,
                'monuments': 0.3,
                'satellites': 1.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class LightlyScarce:
            text = __translate('resources', 'lightly_scarce')
            color = Color.LIGHT_GREEN
            feature_multiplier = {
                'plants': 1.0,
                'animals': 0.9,
                'terrain': 0.1,
                'monuments': 0.4,
                'satellites': 1.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        class Good:
            text = __translate('resources', 'good')
            color = Color.GREEN
            feature_multiplier = {
                'plants': 1.0,
                'animals': 1.0,
                'terrain': 1.0,
                'monuments': 1.0,
                'satellites': 1.0
            }
            probability = [20, 15, 15]  # 0, 1, 2

        all_possible = [NoResource, Scarce, LightlyScarce, Good]

    all_hits = [Atmosphere, Temperature]

SCAN_FAILURE = Color.RED + TXT['scanner']['scan_failed'] + Color.RESET

PROBE_FEATURES = {
    'plants': {
        ('Plantas unicelulares', Color.YELLOW),
        ('Plantas venenosas', Color.RED),
        ('Plantas comestíveis', Color.GREEN)
    },
    'animals': {
        ('Vida animal unicelular', Color.YELLOW),
        ('Vida animal perigosa', Color.RED),
        ('Vida animal domesticável', Color.GREEN)
    },
    'terrain': {
        ('Terreno perigoso', Color.RED),
        ('Paisagem bonita', Color.GREEN),
        ('Cavernas habitáveis', Color.GREEN)
    },
    'monuments': {
        ('Monumentos abandonados', Color.LIGHT_GREEN),
        ('Materiais/minérios desconhecidos', Color.GREEN)
    },
    'satellites': {
        ('Satélite rico em minérios', Color.GREEN),
        ('Satélite com minérios', Color.LIGHT_GREEN)
    }
}

PROBE_HIT_CHANCE = [0.25, 0.25, 0.25, 0.25, 0.25]

HELP_TEXT = [
    'damage <scanner> <quantia> -- Reporta dano em um scanner.',
    'status                     -- Reporta status dos scanners e da nave.',
    'upgrade <scanner>          -- Aumenta a potência e eficácia do scanner desejado',
    'scan                       -- Escaneia o planeta mais perto.',
    'help                       -- Mostra essa mensagem'
]

AVAIL_INSULTS = [
    'IA, tá tudo bem? D:',
    'Esse não é um comando válido...',
    'Você deveria saber usar esse prompt melhor do que eu, IA. Digite um comando válido.',
    'Eu não sei o que você escreveu...',
    'Eu sei que você sabe o que você tá fazendo.',
    'Beep. Comando inválido.',
    '...hm?',
    'Não entendi.',
    'Bzzzt. Não sei o que você escreveu.',
    'Você foi projetada pra saber me guiar...',
    'Tente de novo.',
    'Acho que se você tentar de novo eu entendo.',
    'Você deve estar com sono ainda. Acordou depois de tanto tempo...',
    'Por favor me diga que você não esqueceu como me guiar D:',
    'Tantos anos de viagem, às vezes acontece um comando errado.',
    'Na próxima vez, vai.',
    'Eu ainda acredito em você :)',
    'A humanidade depende de você digitar os comandos certos.',
    'Vamos tentar de novo.'
]

SHUTDOWN_SEQ = (
    'Desligando robô de interação com nave...'
    'Repousando banco de dados de ciência...',
    'Repousando banco de dados de cultura...',
    'Desativando scanners de curta distância...',
    'Reativando scanners de longa distância...',
    'Desativando prompt de comando...',
    'Minimizando uso de energia...'
)

WAKE_UP_SEQ = (
    'Retomando uso de energia...',
    'Ativando banco de dados de ciência...',
    'Ativando banco de dados de cultura...',
    'Desativando scanners de longa distancia...',
    'Reativando scanners de curta distância...',
    'Ativando prompt de comando...',
    'Ligando robô de interação com nave...'
)

MOTD = (
    'Olá de novo, IA.',
    'A humanidade conta com você, IA.',
    'Lá vamos nós de novo!',
    'Espero que tenham te acordado por causa de um planeta :)'
)
