from time import sleep
from planet_scanner import Scanner
import random as r
from settings import CommandError, HELP_TEXT

class Seedship:

    def __init__(self):
        self.planet = None
        self.hits = None
        self.has_probed = False
        self.features = None
        self.scanner = Scanner()

    def damage(self, splitted_line):
        self.__check_length(splitted_line, 3)
        self.scanner.damage_status(splitted_line[1], splitted_line[2])

    def status(self, splitted_line):
        self.__check_length(splitted_line, 1)
        self.scanner.print_status()

    def upgrade(self, splitted_line):
        self.__check_length(splitted_line, 2)
        self.scanner.upgrade_self.scanner(splitted_line[1])

    def help(self, splitted_line):
        self.__print_help()

    def scan(self, splitted_line):
        self.__check_length(splitted_line, 1)
        if not self.planet:
            self.planet = self.scanner.generate_planet()
            self.hits = self.scanner.generate_hits()
            self.has_probed = False
            self.features = None
        self.scanner.print_planet(self.planet, self.hits)

    def probe(self, splitted_line):
        self.__check_length(splitted_line, 1)
        if not self.planet:
            raise CommandError('Você precisa escanear o planeta primeiro!')
        if self.planet and not self.has_probed:
            self.features = self.scanner.generate_planet_features(self.planet)
            self.has_probed = True
        self.scanner.print_planet(self.planet, self.hits, self.has_probed, self.features)

    def __check_length(self, splitted_line, length):
        if len(splitted_line) != length:
            raise CommandError('Esperava ' + str(length - 1) + ' parâmetros,'
                               + ' recebi ' + str(len(splitted_line) - 1))

    def sleep(self, splitted_line):
        self.planet = None
        self.has_probed = False
        self.hits = None
        self.features = None
        self.__cinematic_sleep()

    def __cinematic_sleep(self):
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

    def __print_help(self):
        for line in HELP_TEXT:
            sleep(0.1)
            print(line)


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
