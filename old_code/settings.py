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

AVAIL_HITS = {
    'Atmosfera': [
        (TXT['scanner']['hits']['atmosphere']['corrosive'], Color.RED,         0.1, 0.1, 1.0, 0.4, 1.0), # 0
        (TXT['scanner']['hits']['atmosphere']['none'], Color.RED,              0.1, 0.1, 1.0, 0.4, 1.0), # 1
        (TXT['scanner']['hits']['atmosphere']['rare'], Color.YELLOW,           0.9, 0.9, 1.0, 0.7, 1.0), # 2
        (TXT['scanner']['hits']['atmosphere']['semi_rare'], Color.LIGHT_GREEN, 1.0, 1.0, 1.0, 0.9, 1.0), # 3
        (TXT['scanner']['hits']['atmosphere']['good'], Color.GREEN,            1.2, 1.2, 1.0, 1.0, 1.0), # 4
        (TXT['scanner']['hits']['atmosphere']['unbreathable'], Color.RED,      0.8, 0.1, 1.0, 0.4, 1.0)  # 5
    ],
    'Temperatura': [
        (TXT['scanner']['hits']['temperature']['very_low'], Color.RED,         0.3, 0.9, 1.0, 0.1, 1.0), # 0
        (TXT['scanner']['hits']['temperature']['low'], Color.YELLOW,           0.5, 1.0, 1.0, 0.7, 1.0), # 1
        (TXT['scanner']['hits']['temperature']['good'], Color.GREEN,           1.2, 1.2, 1.0, 1.0, 1.0), # 2
        (TXT['scanner']['hits']['temperature']['high'], Color.YELLOW,          1.0, 1.0, 1.0, 0.7, 1.0), # 3
        (TXT['scanner']['hits']['temperature']['ver_high'], Color.RED,         0.3, 0.3, 1.0, 0.4, 1.0)  # 4
    ],
    'Água': [
        (TXT['scanner']['hits']['water']['none'], Color.RED,                   0.1, 0.1, 0.7, 0.3, 1.0), # 0
        (TXT['scanner']['hits']['water']['trace'], Color.RED,                  0.7, 0.4, 1.0, 0.6, 1.0), # 1
        (TXT['scanner']['hits']['water']['scarce'], Color.YELLOW,              1.0, 0.9, 1.0, 0.7, 1.0), # 2
        (TXT['scanner']['hits']['water']['good'], Color.GREEN,                 1.1, 1.1, 1.0, 1.0, 1.0), # 3
        (TXT['scanner']['hits']['water']['planet_wide_ocean'], Color.YELLOW,   1.0, 1.0, 0.1, 0.4, 1.0)  # 4
    ],
    'Gravidade': [
        (TXT['scanner']['hits']['gravity']['very_low'], Color.RED,             0.1, 0.1, 0.7, 0.3, 0.0), # 0
        (TXT['scanner']['hits']['gravity']['low'], Color.YELLOW,               0.8, 0.8, 1.0, 0.9, 0.3), # 1
        (TXT['scanner']['hits']['gravity']['good'], Color.GREEN,               1.1, 1.1, 1.0, 1.0, 0.7), # 2
        (TXT['scanner']['hits']['gravity']['high'], Color.YELLOW,              0.8, 0.8, 1.0, 0.9, 1.1), # 3
        (TXT['scanner']['hits']['gravity']['very_high'], Color.RED,            0.5, 0.2, 0.7, 0.3, 1.3)  # 4
    ],
    'Recursos': [
        (TXT['scanner']['hits']['resources']['none'], Color.RED,                   1.0, 0.6, 0.7, 0.0, 1.0), # 0
        (TXT['scanner']['hits']['resources']['scarce'], Color.YELLOW,              1.0, 0.9, 1.0, 0.3, 1.0), # 1
        (TXT['scanner']['hits']['resources']['lightly_scarce'], Color.LIGHT_GREEN, 1.0, 1.0, 1.0, 0.6, 1.0), # 2
        (TXT['scanner']['hits']['resources']['good'], Color.GREEN,                 1.0, 1.0, 1.0, 1.0, 1.0)  # 3
    ]
}

SCAN_FAILURE = Color.RED + TXT['scanner']['scan_failed'] + Color.RESET

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
