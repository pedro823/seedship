from language import TXT
from util import Color, SeedshipExecutionError
from logger import Logger
import random as r
from seedship import Scanner
import os
import time


def translate_command(command: str) -> str:
    return TXT['command'].get(command, command).lower()


def translate_phrase(phrase: str) -> str:
    return TXT['messages'].get(phrase, phrase)


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
        def execute(splitted_line, seedship) -> None:
            module_to_damage = splitted_line[1].lower()
            translated_modules = {}

            for module_list in seedship.modules:
                for module in module_list.values():
                    translated_modules[module.name.lower()] = module

            translated_modules[seedship.colonists.__class__.name.lower()] = seedship.colonists

            if module_to_damage not in translated_modules:
                raise SeedshipExecutionError('module_doesnt_exist')

            try:
                amount = int(splitted_line[2])
            except ValueError:
                raise SeedshipExecutionError('invalid_amount')

            translated_modules[module_to_damage].damage(amount)
            Logger.log_damage(seedship, {'module': module_to_damage, 'amount': amount})

    class Waste:
        command = translate_command('waste')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            consumable_to_waste = splitted_line[1].lower()
            translated_consumables = {consumable.name.lower(): consumable
                                      for consumable in seedship.consumables}

            if consumable_to_waste not in translated_consumables:
                raise SeedshipExecutionError('consumable_doesnt_exist')

            try:
                amount = int(splitted_line[2])
            except ValueError:
                raise SeedshipExecutionError('invalid_amount')

            translated_consumables[consumable_to_waste].waste(amount)
            Logger.log_waste(seedship, {'consumable': consumable_to_waste, 'amount': amount})

    class Regenerate:
        command = translate_command('regenerate')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            to_be_regenerated = splitted_line[1].lower()

            try:
                amount = int(splitted_line[2])
            except ValueError:
                raise SeedshipExecutionError('invalid_amount')

            # to_be_regenerated should be consumable or a database
            regenerable = {consumable.name.lower(): consumable
                           for consumable in seedship.consumables}
            regenerable.update({database.name.lower(): database
                                for database in seedship.databases.values()})

            print(regenerable)
            if to_be_regenerated not in regenerable:
                raise SeedshipExecutionError('not_regenerable')

            regenerable[to_be_regenerated].regenerate(amount)

    class Status:
        command = translate_command('status')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            for module_list in seedship.modules:
                has_printed_module_list_name = False
                for module in module_list.values():
                    health_color = module.get_color()
                    health = module.health
                    str_left = f'{Color.RESET}{module.name.capitalize()}: '
                    str_right = f'{health_color}{health}%{Color.RESET}'
                    string = str_left.ljust(20) + str_right.ljust(18)
                    if isinstance(module, Scanner):
                        string += f'({module.upgrade_level})'
                    if not has_printed_module_list_name:
                        time.sleep(0.4)
                        print(f'{module.__class__.name}:')
                        time.sleep(0.2)
                        has_printed_module_list_name = True
                    print(f'\t{string}')
                    time.sleep(0.2)

            has_printed_consumable_name = False
            for consumable in seedship.consumables:
                amount_color = consumable.get_color()
                str_left = f'{Color.RESET}{consumable.name.capitalize()}: '
                str_right = f'{amount_color}{consumable.amount}{Color.RESET}'
                string = str_left.ljust(20) + str_right.ljust(18)
                if not has_printed_consumable_name:
                    time.sleep(0.4)
                    print(f'{consumable.__class__.name}:')
                    time.sleep(0.2)
                    has_printed_consumable_name = True
                print(f'\t{string}')
                time.sleep(0.2)

            if seedship.colonists < 100:
                colonists_color = Color.RED + Color.BLINK
            elif seedship.colonists < 400:
                colonists_color = Color.LIGHT_RED
            elif seedship.colonists < 800:
                colonists_color = Color.YELLOW
            elif seedship.colonists < 900:
                colonists_color = Color.LIGHT_GREEN
            else:
                colonists_color = Color.GREEN
            translated_colonists = seedship.colonists.__class__.name
            print(f'{translated_colonists}: {colonists_color}{seedship.colonists}{Color.RESET}')
            time.sleep(0.3)
            print(f'{TXT["status"]["probes_left"]}: {seedship.probes_left}')

    class Land:
        command = translate_command('land')
        argument_count = 0

        @classmethod
        def execute(cls, splitted_line, seedship) -> bool:
            are_you_sure = translate_phrase('are_you_sure')
            yes = translate_phrase('yes').lower()
            no = translate_phrase('no')
            confirmation = input(f'{are_you_sure} ({yes[0]}/{no[0].upper()})').strip().lower()
            if confirmation != '' and confirmation in yes.lower():
                cls.__print_landing_sequence()
                return True
            print(translate_phrase('land_confirmation_no'))
            return False

        @staticmethod
        def __print_landing_sequence():
            phases = ['space', 'atmosphere', 'glide', 'touchdown']
            print_queue = []
            looking_to_print_list = []
            time.sleep(2.8)
            # TODO cinematics

    class Upgrade:
        command = translate_command('upgrade')
        argument_count = 1

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            scanners = {scanner.name.lower(): scanner
                        for scanner in seedship.scanners.values()}
            scanner_to_upgrade = splitted_line[1].lower()

            if scanner_to_upgrade not in scanners:
                raise SeedshipExecutionError('scanner_doesnt_exist')

            scanners[scanner_to_upgrade].upgrade()

    class Help:
        command = translate_command('help')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            for text in TXT['help_text'].values():
                print(text)
                time.sleep(0.2)

    class Scan(PlanetRelatedCommand):
        command = translate_command('scan')
        argument_count = 0

        @classmethod
        def execute(cls, splitted_line, seedship) -> None:
            scan_result = seedship.scan_planet()
            cls.print_scan_result(scan_result)

    class Probe(PlanetRelatedCommand):
        command = translate_command('probe')
        argument_count = 0

        NO_LANDSCAPE = TXT['landscape']['no_landscape']

        @classmethod
        def execute(cls, splitted_line, seedship) -> None:
            scan_result = seedship.probe_planet()
            Logger.log_probe(seedship.probes_left)
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
        def execute(splitted_line, seedship) -> None:
            for shutdown_text in TXT['shutdown_sequence']:
                print(shutdown_text)
                time.sleep(0.15)
            enter_to_wake_up = translate_phrase('enter_to_wake_up')
            input(f'[{enter_to_wake_up.upper()}]')
            seedship.find_new_planet()
            seedship.deal_trace_damage()
            Logger.log_planet(seedship.planet)
            for wake_up_sequence in TXT['shutdown_sequence']:
                print(wake_up_sequence)
                time.sleep(0.15)
            time.sleep(0.3)
            print(r.choice(TXT['wake_up_messages']))

    class Clear:
        command = translate_command('clear')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            os.system('cls') if os.name == 'nt' else os.system('clear')

    class Idle:
        command = ''
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship) -> None:
            pass

    class Exit:
        command = translate_command('exit')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship) -> bool:
            return True

    class Roll:
        command = translate_command('roll')
        argument_count = -1

        class RollException(SeedshipExecutionError):

            def __init__(self, message: str, dice: str):
                super().__init__(message)
                self.dice = dice

        @classmethod
        def execute(cls, splitted_line, seedship) -> None:
            translated_sum = TXT['messages'].get('sum_die', 'Sum of die')
            for amount, faces in cls.parse_dice(splitted_line):
                sum_dice = 0
                print('-' * 10 + f' {amount}d{faces}:')
                for dice in range(1, amount + 1):
                    if faces < 1:
                        raise cls.RollException('invalid_dice', f'{amount}d{faces}')
                    roll = r.randint(1, faces)
                    print(Color.LIGHT_BLUE
                          + f'{amount}d{faces}: '
                          + Color.YELLOW
                          + f'#{dice}: '
                          + Color.RESET
                          + f'{roll}')
                    sum_dice += roll
                print(f'{translated_sum}: {sum_dice}')
            print('-' * 10)

        @classmethod
        def parse_dice(cls, splitted_line: list) -> list:
            formatted_line = [dice.split('d') for dice in splitted_line[1:]]
            for i in formatted_line:
                try:
                    yield int(i[0]), int(i[1])
                except ValueError:
                    raise cls.RollException(f'invalid_dice', 'd'.join(i))

    all = [Damage, Status, Upgrade, Help, Scan, Regenerate,
           Probe, Sleep, Clear, Waste, Idle, Land, Roll]
    all_commands = [c.command for c in all]
    command_to_class = dict(zip(all_commands, all))

    @classmethod
    def is_command(cls, command):
        return command in cls.all_commands
