from random import SystemRandom as random
import os
r = random()

YELLOW = '\033[1;33m'
LIGHT_BLUE = '\033[1;34m'
LIGHT_RED = '\033[1;31m'
CLEAR = '\033[0;37m'


def dice_roll(parsed_line):
    all_sum = 0
    for roll in parsed_line:
        print('-' * 40)
        amount = roll[0]
        faces = roll[1]
        all_rolls = [r.randint(1, faces) for _ in range(amount)]
        for index, single_roll in enumerate(all_rolls):
            print(LIGHT_BLUE
                  + str(amount) + 'd' + str(faces) + ':'
                  + YELLOW
                  + ' Roll #' + str(index + 1) + ': '
                  + CLEAR
                  + str(single_roll))
        single_sum = sum(all_rolls)
        print(YELLOW,
              '\tPARTIAL SUM:',
              single_sum,
              CLEAR)
        all_sum += single_sum
    print('-' * 40)
    print(LIGHT_RED + 'TOTAL SUM:', all_sum, CLEAR)

def parse_line(line):
    formatted_line = [dice.split('d') for dice in line.split(' ')]
    integer_line = [[int(i[0]), int(i[1])] for i in formatted_line]
    for dice_roll in formatted_line:
        print('Rolling', dice_roll[0], dice_roll[1] + '-faced dice.')
    return integer_line

while True:
    try:
        line = input('>>> ').strip()
        _ = os.system('cls' if os.name == 'nt' else 'clear')
        if line == 'quit()':
            break
        if line == '':
            continue
        parsed_line = parse_line(line)
        dice_roll(parsed_line)
    except EOFError:
        break
    except KeyboardInterrupt:
        break
    except Exception as ex:
        print(str(ex))
