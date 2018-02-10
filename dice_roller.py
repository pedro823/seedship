from random import SystemRandom as random
from settings import Color
import os
r = random()

def dice_roll(parsed_line):
    all_sum = 0
    for roll in parsed_line:
        print('-' * 40)
        amount = roll[0]
        faces = roll[1]
        all_rolls = [r.randint(1, faces) for _ in range(amount)]
        for index, single_roll in enumerate(all_rolls):
            print(Color.LIGHT_BLUE
                  + str(amount) + 'd' + str(faces) + ':'
                  + Color.YELLOW
                  + ' Roll #' + str(index + 1) + ': '
                  + Color.RESET
                  + str(single_roll))
        single_sum = sum(all_rolls)
        print(Color.YELLOW,
              '\tPARTIAL SUM:',
              single_sum,
              Color.RESET)
        all_sum += single_sum
    print('-' * 40)
    print(Color.LIGHT_RED + 'TOTAL SUM:', all_sum, Color.RESET)

def parse_line(line):
    formatted_line = [dice.split('d') for dice in line.split(' ')]
    integer_line = [[int(i[0]), int(i[1])] for i in formatted_line]
    for dice_roll in formatted_line:
        print('Rolling', dice_roll[0], dice_roll[1] + '-faced dice.')
    return integer_line

if __name__ == '__main__':
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
