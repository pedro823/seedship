from dice_roller import dice_roll, parse_line
from planet_scanner import Scanner, Error, print_noln
from settings import *
import random as r
import os
from time import sleep
from seedship import Seedship, AVAIL_COMMANDS

class Prompt:
    def __init__(self, seedship):
        self.seedship = seedship

    def cinematic_sleep(self):
        print_noln('Preparando para dormir')
        for i in range(2):
            sleep(0.1)
            print_noln('.')
        sleep(0.1)
        print('.')
        for line in SHUTDOWN_SEQ:
            print(line)
            sleep(0.15)
        sleep(1)
        self.__clear_screen()
        print('[PRESSIONE ENTER PARA ACORDAR]')
        input()
        for line in WAKE_UP_SEQ:
            print(line)
            sleep(0.15)
        sleep(1)
        print(r.choice(MOTD))

    def is_command(self, line):
        return line.split(' ')[0] in AVAIL_COMMANDS

    def exec_command(self, line):
        splitted_line = line.split(' ')
        if splitted_line[0] == 'damage':
            self.scanner.damage_status(splitted_line[1], splitted_line[2])
        elif splitted_line[0] == 'status':
            self.scanner.print_status()
        elif splitted_line[0] == 'upgrade':
            self.scanner.upgrade_self.scanner(splitted_line[1])
            self.scanner.print_status()
        elif splitted_line[0] == 'scan':
            if not self.planet:
                self.planet = self.scanner.generate_planet()
                self.hits = self.scanner.generate_hits()
                self.has_probed = False
                self.features = None
            self.scanner.print_planet(self.planet, self.hits)
        elif splitted_line[0] == 'rescan':
            if self.has_probed:
                self.scanner.print_planet(self.planet, self.hits, self.has_probed, self.features)
            else:
                self.scanner.print_planet(self.planet, self.hits)
        elif splitted_line[0] == 'probe':
            if self.planet and not self.has_probed:
                self.features = self.scanner.generate_planet_features(self.planet)
                self.has_probed = True
            self.scanner.print_planet(self.planet, self.hits, self.has_probed, self.features)
        elif splitted_line[0] == 'help':
            self.print_help()
        elif splitted_line[0] == 'sleep':
            self.planet = None
            self.has_probed = False
            self.hits = None
            self.features = None
            self.cinematic_sleep()
        elif splitted_line[0] == 'exit':
            sleep(0.3)
            print('Obrigado por tudo, IA.')
            return True
        return False

    def print_help(self):
        for line in HELP_TEXT:
            sleep(0.1)
            print(line)

    @staticmethod
    def __clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')


prompt = Prompt(Seedship())
while True:
    try:
        line = input('sdshp> ').strip()
        if line == 'quit()':
            break
        if line == '':
            continue
        if prompt.is_command(line):
            try:
                if prompt.exec_command(line):
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
    except EOFError:
        break
    except KeyboardInterrupt:
        break
    except Exception as ex:
        print(str(ex))
