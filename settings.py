class Error(Exception):
    class NoSuchScanner:
        pass
    class CannotUpgrade:
        pass
    class BadConfig:
        pass
    class CommandError:
        pass

class Color:
    BLACK =        '\033[0;30m'
    GRAY =         '\033[1;30m'
    RED =          '\033[0;31m'
    LIGHT_RED =    '\033[1;31m'
    GREEN =        '\033[0;32m'
    LIGHT_GREEN =  '\033[1;32m'
    BROWN =        '\033[0;33m'
    YELLOW =       '\033[1;33m'
    BLUE =         '\033[0;34m'
    LIGHT_BLUE =   '\033[1;34m'
    PURPLE =       '\033[0;35m'
    LIGHT_PURPLE = '\033[1;35m'
    CYAN =         '\033[0;36m'
    LIGHT_CYAN =   '\033[1;36m'
    LIGHT_GRAY =   '\033[0;37m'
    WHITE =        '\033[1;37m'
    RESET =        '\033[0m'

SCAN_SETTINGS = {
    'atmosfera': [
        [10, 30, 50, 65, 80], # level 0
        [5, 15, 25, 50, 90], # level 1
        [0, 0, 5, 35, 95]  # level 2
    ],
    'temperatura': [
        [20, 40, 60, 80], # level 0
        [5, 30, 70, 95],  # level 1
        [0, 15, 85]       # level 2
    ],
    'água': [
        [20, 40, 60, 80], # level 0
        [5, 20, 40, 85], # level 1
        [0, 5, 15, 90]  # level 2
    ],
    'gravidade': [
        [20, 40, 60, 80], # level 0
        [5, 30, 70, 95],  # level 1
        [0, 15, 85]       # level 2
    ],
    'recursos': [
        [25, 50, 75], # level 0
        [0, 30, 60], # level 1
        [0, 5, 40]  # level 2
    ]
}

AVAIL_OPTIONS = {
    'atmosfera': [
        ('Corrosiva', Color.RED,                        0.1, 0.1, 1.0, 0.4, 1.0), # 0
        ('Nenhuma', Color.RED,                          0.1, 0.1, 1.0, 0.4, 1.0), # 1
        ('Rarefeita', Color.YELLOW,                     0.9, 0.9, 1.0, 0.7, 1.0), # 2
        ('Levemente Rarefeita', Color.LIGHT_GREEN,      1.0, 1.0, 1.0, 0.9, 1.0), # 3
        ('Ótima', Color.GREEN,                          1.2, 1.2, 1.0, 1.0, 1.0), # 4
        ('Não Respirável', Color.RED,                   0.8, 0.1, 1.0, 0.4, 1.0)  # 5
    ],
    'temperatura': [
        ('Muito Baixa', Color.RED,                      0.3, 0.9, 1.0, 0.1, 1.0), # 0
        ('Baixa', Color.YELLOW,                         0.5, 1.0, 1.0, 0.7, 1.0), # 1
        ('Boa', Color.GREEN,                            1.2, 1.2, 1.0, 1.0, 1.0), # 2
        ('Alta', Color.YELLOW,                          1.0, 1.0, 1.0, 0.7, 1.0), # 3
        ('Muito Alta', Color.RED,                       0.3, 0.3, 1.0, 0.4, 1.0)  # 4
    ],
    'água': [
        ('Nenhuma', Color.RED,                          0.1, 0.1, 0.7, 0.3, 1.0), # 0
        ('Traços', Color.RED,                           0.7, 0.4, 1.0, 0.6, 1.0), # 1
        ('Escassa', Color.YELLOW,                       1.0, 0.9, 1.0, 0.7, 1.0), # 2
        ('Plena', Color.GREEN,                          1.1, 1.1, 1.0, 1.0, 1.0), # 3
        ('Planeta coberto de oceanos', Color.YELLOW,    1.0, 1.0, 0.1, 0.4, 1.0)  # 4
    ],
    'gravidade': [
        ('Muito Baixa', Color.RED,                      0.1, 0.1, 0.7, 0.3, 0.0), # 0
        ('Baixa', Color.YELLOW,                         0.8, 0.8, 1.0, 0.9, 0.3), # 1
        ('Boa', Color.GREEN,                            1.1, 1.1, 1.0, 1.0, 0.7), # 2
        ('Alta', Color.YELLOW,                          0.8, 0.8, 1.0, 0.9, 1.1), # 3
        ('Muito Alta', Color.RED,                       0.5, 0.2, 0.7, 0.3, 1.3)  # 4
    ],
    'recursos': [
        ('Nenhum', Color.RED,                           1.0, 0.6, 0.7, 0.0, 1.0), # 0
        ('Escassos', Color.YELLOW,                      1.0, 0.9, 1.0, 0.3, 1.0), # 1
        ('Levemente escassos', Color.LIGHT_GREEN,       1.0, 1.0, 1.0, 0.6, 1.0), # 2
        ('Plenos', Color.GREEN,                         1.0, 1.0, 1.0, 1.0, 1.0)  # 3
    ]
}

SCAN_FAILURE = Color.RED + "Scan falhado." + Color.RESET

PROBE_FEATURES = [
    {
        ('Plantas unicelulares', Color.YELLOW),
        ('Plantas venenosas', Color.RED),
        ('Plantas comestíveis', Color.GREEN)
    },
    {
        ('Vida animal unicelular', Color.YELLOW),
        ('Vida animal perigosa', Color.RED),
        ('Vida animal domesticável', Color.GREEN)
    },
    {
        ('Terreno perigoso', Color.RED),
        ('Paisagem bonita', Color.GREEN),
        ('Cavernas habitáveis', Color.GREEN)
    },
    {
        ('Monumentos abandonados', Color.LIGHT_GREEN),
        ('Materiais/minérios desconhecidos', Color.GREEN)
    },
    {
        ('Satélite rico em minérios', Color.GREEN),
        ('Satélite com minérios', Color.LIGHT_GREEN)
    }
]

PROBE_HIT_CHANCE = [0.25, 0.25, 0.25, 0.25, 0.25]

AVAIL_COMMANDS = {
    'damage',
    'status',
    'upgrade',
    'scan',
    'rescan',
    'probe',
    'help',
    'sleep',
    'exit'
}

AVAIL_INSULTS = [
    'IA, tá tudo bem? D:',
    'Esse não é um comando válido...',
    'Você deveria saber usar esse prompt melhor do que eu, IA. Digite um comando válido.',
    'Eu não sei o que você escreveu...',
    'Eu sei que você sabe o que você tá fazendo.',
    'Beep. Comando inválido.',
    '...hm?',
    'Não entendi.',
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
    'Desligando banco de dados de ciência...',
    'Desligando banco de dados de cultura...',
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
    'A humanidade conta em você, IA.',
    'Espero que tenham te acordado por causa de um planeta :)'
)
