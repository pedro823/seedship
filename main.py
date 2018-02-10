from dice_roller import dice_roll, parse_line
from planet_scanner import Scanner, Error, print_noln
from settings import *
import random as r
from time import sleep

PLANET = None
HITS = None
HAS_PROBED = False
FEATURES = None
scanner = Scanner()

def cinematic_sleep():
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
    _ = os.system('cls' if os.name == 'nt' else 'clear')
    print('[PRESSIONE ENTER PARA ACORDAR]')
    input()
    for line in WAKE_UP_SEQ:
        print(line)
        sleep(0.15)
    sleep(1)
    print(r.choice(MOTD))

def is_command(line):
    return line.split(' ')[0] in AVAIL_COMMANDS

def exec_command(line, scanner):
    splitted_line = line.split(' ')
    if splitted_line[0] == 'damage':
        scanner.damage_status(splitted_line[1], splitted_line[2])
    elif splitted_line[0] == 'status':
        scanner.print_status()
    elif splitted_line[0] == 'upgrade':
        scanner.upgrade_scanner(splitted_line[1])
        scanner.print_status()
    elif splitted_line[0] == 'scan':
        if PLANET:
            PLANET = scanner.generate_planet()
            HITS = scanner.generate_hits()
            HAS_PROBED = False
            FEATURES = None
        scanner.print_planet(PLANET, HITS)
    elif splitted_line[0] == 'rescan':
        if HAS_PROBED:
            scanner.print_planet(PLANET, HITS, HAS_PROBED, FEATURES)
        else:
            scanner.print_planet(PLANET, HITS)
    elif splitted_line[0] == 'probe':
        if PLANET and not HAS_PROBED:
            FEATURES = scanner.generate_planet_features(PLANET)
            HAS_PROBED = True
        scanner.print_planet(PLANET, HITS, HAS_PROBED, FEATURES)
    elif splitted_line[0] == 'help':
        print_help()
    elif splitted_line[0] == 'sleep':
        PLANET = None
        HAS_PROBED = False
        HITS = None
        FEATURES = None
        cinematic_sleep()
    elif splitted_line[0] == 'exit':
        sleep(0.3)
        print('Obrigado por tudo, IA.')
        return True
    return False

while True:
    try:
        line = input('sdshp> ').strip()
        if line == 'quit()':
            break
        if line == '':
            continue
        if is_command(line):
            try:
                if exec_command(line, scanner):
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
                sleep(0.6)
                print(r.choice(AVAIL_INSULTS))
    except EOFError:
        break
    except KeyboardInterrupt:
        break
    except Exception as ex:
        print(str(ex))
