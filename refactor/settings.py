from util import Color
from language import TXT

SCAN_FAILURE = Color.RED + TXT['scanner']['scan_failed'] + Color.RESET


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
