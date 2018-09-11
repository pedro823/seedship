from language import TXT
from util import Color
import random as r
from seedship import Scanner
import os
import time


def translate_command(command):
    return TXT['command'].get(command, command).lower()


class PlanetRelatedCommand:
    @classmethod
    def print_scan_result(cls, scan_result):
        for planet_feature, feature_value in scan_result.features.items():
            cls.__print_noln(cls.__translate_feature(planet_feature))
            for i in range(3):
                time.sleep(0.14)
                cls.__print_noln('.')
            time.sleep(0.5)
            print(f' {feature_value.color}{feature_value.text}{Color.RESET}')
            time.sleep(0.3)

    @staticmethod
    def __print_noln(*args, **kwargs):
        print(end='', flush=True, *args, **kwargs)

    @staticmethod
    def __translate_feature(feature: str) -> str:
        ''' Translates planet's feature '''
        return TXT['scanner']['categories'].get(feature, feature)


class AvailableCommands:
    class Damage:
        command = translate_command('damage')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship):
            module_to_damage = splitted_line[1].lower()
            translated_modules = {}

            for module_list in seedship.modules:
                for module in module_list.values():
                    translated_modules[module.name.lower()] = module

            if module_to_damage not in translated_modules:
                raise Exception(f'module={splitted_line[1]} doesn\'t exist')

            amount = int(splitted_line[2])
            translated_modules[module_to_damage].damage(amount)

    class Status:
        command = translate_command('status')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship):
            for module_list in seedship.modules:
                has_printed_module_list_name = False
                for module in module_list.values():
                    health = module.health
                    if health < 40:
                        status_color = Color.LIGHT_RED
                    elif health < 70:
                        status_color = Color.YELLOW
                    elif health < 95:
                        status_color = Color.LIGHT_GREEN
                    else:
                        status_color = Color.GREEN
                    str_left = f'{Color.RESET}{module.name.capitalize()}: '
                    str_right = f'{status_color}{health}%{Color.RESET}'
                    string = str_left.ljust(17) + str_right.ljust(18)
                    if isinstance(module, Scanner):
                        string += f'({module.upgrade_level})'
                    if not has_printed_module_list_name:
                        time.sleep(0.4)
                        print(f'{module.__class__.name}:')
                        time.sleep(0.2)
                        has_printed_module_list_name = True
                    print(f'\t{string}')
                    time.sleep(0.2)
            print(f'{TXT["status"]["probes_left"]}: {seedship.probes_left}')

    class Upgrade:
        command = translate_command('upgrade')
        argument_count = 1

        @staticmethod
        def execute(parsed_line, seedship):
            scanners = dict((scanner.name.lower(), scanner)
                            for scanner in seedship.scanners.values())
            scanner_to_upgrade = parsed_line[1].lower()

            if scanner_to_upgrade not in scanners:
                raise Exception(f'scanner={scanner_to_upgrade} doesn\'t exist')

            scanners[scanner_to_upgrade].upgrade()

    class Help:
        command = translate_command('help')
        argument_count = 0

        @staticmethod
        def execute(parsed_line, seedship):
            for text in TXT['help_text'].values():
                print(text)
                time.sleep(0.2)

    class Scan(PlanetRelatedCommand):
        command = translate_command('scan')
        argument_count = 0

        @classmethod
        def execute(cls, parse_line, seedship):
            scan_result = seedship.scan_planet()
            cls.print_scan_result(scan_result)

    class Probe(PlanetRelatedCommand):
        command = translate_command('probe')
        argument_count = 0

        NO_LANDSCAPE = TXT['landscape']['no_landscape']

        @classmethod
        def execute(cls, parse_line, seedship):
            scan_result = seedship.probe_planet()
            cls.print_scan_result(scan_result)
            time.sleep(0.25)
            print()
            time.sleep(0.25)
            cls.__print_landscape(scan_result)

        @classmethod
        def __print_landscape(cls, scan_result):
            ''' Prints the landscape of the planet '''
            if scan_result.landscape == []:
                print(cls.NO_LANDSCAPE)
            else:
                for landscape in scan_result.landscape:
                    print(f'{landscape.color}{landscape.text}{Color.RESET}')
                    time.sleep(0.4)

    class Sleep:
        command = translate_command('sleep')
        argument_count = 0

        @staticmethod
        def execute(parsed_line, seedship):
            for shutdown_text in TXT['shutdown_sequence']:
                print(shutdown_text)
                time.sleep(0.15)
            input('[PRESS ENTER TO WAKE UP]')
            seedship.find_new_planet()
            for wake_up_sequence in TXT['shutdown_sequence']:
                print(wake_up_sequence)
                time.sleep(0.15)
            time.sleep(0.3)
            print(r.choice(TXT['wake_up_messages']))

    class Clear:
        command = translate_command('clear')
        argument_count = 0

        @staticmethod
        def execute(parsed_line, seedship):
            os.system('cls') if os.name == 'nt' else os.system('clear')

    class Idle:
        command = ''
        argument_count = 0

        @staticmethod
        def execute(parsed_line, seedship):
            pass

    all = [Damage, Status, Upgrade, Help, Scan, Probe, Sleep, Clear, Idle]
    all_commands = [c.command for c in all]
    command_to_class = dict((name, command) for name, command in zip(all_commands, all))

    @classmethod
    def is_command(cls, command):
        return command in cls.all_commands
