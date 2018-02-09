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
        ('Corrosiva', Color.RED,                        0.1, 0.1, 1.0, 1.0), # 0
        ('Nenhuma', Color.RED,                          0.1, 0.1, 1.0, 1.0), # 1
        ('Rarefeita', Color.YELLOW,                     0.9, 0.9, 1.0, 1.0), # 2
        ('Levemente Rarefeita', Color.LIGHT_GREEN,      1.0, 1.0, 1.0, 1.0), # 3
        ('Ótima', Color.GREEN,                          1.2, 1.2, 1.0, 1.0), # 4
        ('Não Respirável', Color.RED,                   0.8, 0.1, 1.0, 1.0) # 5
    ],
    'temperatura': [
        ('Muito Baixa', Color.RED,                      0.3, 0.9, 1.0, 1.0), # 0
        ('Baixa', Color.YELLOW,                         0.5, 1.0, 1.0, 1.0), # 1
        ('Boa', Color.GREEN,                            1.2, 1.2, 1.0, 1.0), # 2
        ('Alta', Color.YELLOW,                          1.0, 1.0, 1.0, 1.0), # 3
        ('Muito Alta', Color.RED,                       0.3, 0.3, 1.0, 1.0) # 4
    ],
    'água': [
        ('Nenhuma', Color.RED,                          0.1, 0.1, 0.7, 0.7), # 0
        ('Traços', Color.RED,                           0.7, 0.4. 1.0, 1.0), # 1
        ('Escassa', Color.YELLOW,                       1.0, 0.9, 1.0, 1.0), # 2
        ('Plena', Color.GREEN,                          1.0, 1.0, 1.0, 1.0), # 3
        ('Planeta coberto de oceanos', Color.YELLOW,    1.0, 1.0, 0.1, 1.0) # 4
    ],
    'gravidade': [
        ('Muito Baixa', Color.RED,                      0.1, 0.1, 0.7, 0.0), # 0
        ('Baixa', Color.YELLOW,                         0.8, 0.8, 1.0, 0.4), # 1
        ('Boa', Color.GREEN,                            1.1, 1.1, 1.0, 1.0), # 2
        ('Alta', Color.YELLOW,                          ), # 3
        ('Muito Alta', Color.RED) # 4
    ],
    'recursos': [
        ('Nenhum', Color.RED), # 0
        ('Escassos', Color.YELLOW), # 1
        ('Levemente escassos', Color.LIGHT_GREEN), # 2
        ('Plenos', Color.GREEN) # 3
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
        ('Satélite rico em minérios', Color.GREEN),
        ('Satélite com minérios', Color.LIGHT_GREEN),
        ('Materiais/minérios desconhecidos', Color.YELLOW)
    }
]

PROBE_HIT_CHANCE = []
