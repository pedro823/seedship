from settings import AVAIL_COMMANDS, AVAIL_INSULTS
import random as r
from time import sleep


class Prompt:

    @classmethod
    def is_command(cls, line):
        return line.split(' ')[0] in AVAIL_COMMANDS

    @classmethod
    def serve(cls):
        while True:
            line = input('sdshp> ').strip()
            if line == 'quit()':
                break
            if line == '':
                continue
            if cls.is_command():
                try:
                    if cls.exec_command(line):
                        break
                except Exception as ex:
                    for line in str(ex).split('\n'):
                        sleep(0.1)
                        print(line)
                    sleep(0.3)
                    print('-' * 20)
                    print(r.choice(AVAIL_INSULTS))
            else:
                try:
                    parsed_line = parse_line(line)
                    dice_roll(parsed_line)
                except ValueError:
                    sleep(0.3)
                    print('Isso não é um comando válido!')
                    sleep(0.6)
                    print(r.choice(AVAIL_INSULTS))
