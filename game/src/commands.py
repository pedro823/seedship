from .language import TXT
from .util import Color, SeedshipExecutionError
from .logger import Logger
from .game_stats import GameStats
from .landscape import AvailableLandscape
from .features import AvailableFeatures
from .seedship import Seedship, Scanner
import random as r
import pickle
import os
import time


def translate_command(command: str) -> str:
    return TXT['command'].get(command, command).lower()


def translate_phrase(phrase: str) -> str:
    return TXT['messages'].get(phrase, phrase)


class DiceParser:

    class RollException(SeedshipExecutionError):

        def __init__(self, message: str, dice: str):
            super().__init__(message)
            self.dice = dice

    class Dice:
        
        def __init__(self, amount: int, faces: int):
            self.amount, self.faces = amount, faces

        def __str__(self):
            return f'{self.amount}d{self.faces}'

    @classmethod
    def parse_int_or_dice(cls, string: str) -> int:
        try:
            return int(string)
        except ValueError:
            return cls.roll_dice(cls.parse_dice(string))

    @classmethod
    def roll_dice(cls, parsed_dice: Dice) -> list:
        amount, faces = parsed_dice.amount, parsed_dice.faces
        sum_of_dice = sum(r.randint(1, faces) for _ in range(amount))
        print(f'{Color.LIGHT_GRAY}{parsed_dice} => {sum_of_dice}{Color.RESET}')
        return sum_of_dice

    @classmethod
    def parse_dice(cls, string: str) -> Dice:
        splitted_string = string.split('d')
        if len(splitted_string) != 2:
            raise cls.RollException('invalid_dice', string)
        
        try:
            amount, faces = map(int, splitted_string)
            if amount <= 0 or faces <= 0:
                raise ValueError()
            return cls.Dice(amount, faces)

        except ValueError:
            raise cls.RollException('invalid_dice', string)

    @classmethod
    def get_dice(cls, splitted_line: list):
        for dice in splitted_line[1:]: # strips command
            try:
                yield cls.parse_dice(dice)
            except ValueError:
                raise cls.RollException(f'invalid_dice', dice)

class PlanetRelatedCommand:
    @classmethod
    def print_scan_result(cls, scan_result):
        for planet_feature, feature_value in scan_result.features.items():
            cls.__print_noln(cls.__translate_feature(planet_feature))
            for _ in range(3):
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
    class Save:
        command = translate_command('save')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            with open('log/seedship_save.pyc', 'wb') as f:
                pickle.dump(seedship, f)
            with open('log/stats_save.pyc', 'wb') as f:
                pickle.dump(stats, f)

    class Load:
        command = translate_command('load')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> (Seedship, GameStats):
            with open('log/seedship_save.pyc', 'rb') as f:
                seedship = pickle.load(f)
            with open('log/stats_save.pyc', 'rb') as f:
                stats = pickle.load(f)
            return seedship, stats

    class Damage:
        command = translate_command('damage')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            module_to_damage = splitted_line[1].lower()
            translated_modules = {}

            for module_list in seedship.modules:
                for module in module_list.values():
                    translated_modules[module.name.lower()] = module

            translated_modules[seedship.colonists.__class__.name.lower()] = seedship.colonists

            if module_to_damage not in translated_modules:
                raise SeedshipExecutionError('module_doesnt_exist')

            try:
                amount = DiceParser.parse_int_or_dice(splitted_line[2])
            except:
                raise SeedshipExecutionError('invalid_amount')

            translated_modules[module_to_damage].damage(amount)
            stats.total_damage_taken += amount
            Logger.log_damage(seedship, {'module': module_to_damage, 'amount': amount})

    class Waste:
        command = translate_command('waste')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            consumable_to_waste = splitted_line[1].lower()
            try:
                amount = DiceParser.parse_int_or_dice(splitted_line[2])
            except:
                raise SeedshipExecutionError('invalid_amount')

            translated_consumables = {consumable.name.lower(): consumable
                                      for consumable in seedship.consumables}
            # can also waste probes
            # TODO change probes into a consumable
            translated_probes = TXT['status']['probes_left'].lower()

            if consumable_to_waste == translated_probes:
                seedship.probes_left = max(0, seedship.probes_left - amount)
                Logger.log_waste(seedship, {'consumable': consumable_to_waste, 'amount': amount})
            elif consumable_to_waste in translated_consumables:
                translated_consumables[consumable_to_waste].waste(amount)
                stats.total_fuel_wasted += amount
                Logger.log_waste(seedship, {'consumable': consumable_to_waste, 'amount': amount})
            else:
                raise SeedshipExecutionError('consumable_doesnt_exist')

    class Evade:
        command = translate_command('evade')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            translated_confirmation = translate_phrase('evade_confirmation')
            print(translated_confirmation)
            seedship.evade_colision()

    class Repair:
        command = translate_command('repair')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            to_be_repaired = splitted_line[1].lower()

            try:
                amount = int(splitted_line[2])
            except ValueError:
                raise SeedshipExecutionError('invalid_amount')

            # to_be_repaired should be consumable or a database
            repairable = {consumable.name.lower(): consumable
                           for consumable in seedship.consumables}
            repairable.update({database.name.lower(): database
                                for database in seedship.databases.values()})

            if to_be_repaired not in repairable:
                raise SeedshipExecutionError('not_repairable')

            repairable[to_be_repaired].repair(amount)

    class Status:
        command = translate_command('status')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
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
        def execute(cls, splitted_line, seedship, stats: GameStats) -> bool:
            are_you_sure = translate_phrase('are_you_sure')
            yes = translate_phrase('yes').lower()
            no = translate_phrase('no')
            confirmation = input(f'{are_you_sure} ({yes[0]}/{no[0].upper()}): ').strip().lower()
            if confirmation != '' and confirmation in yes.lower():
                stats.end_game()
                cls.__print_landing_sequence(seedship)

                print(TXT['stats'].get('you_have_landed', '').center(80, ' '))
                return True

            print(translate_phrase('land_confirmation_no'))
            return False

        @classmethod
        def __print_landing_sequence(cls, seedship):
            looking_to_print_list = []
            landing_sequence_text = TXT['landing_sequence']['landing_system']
            failure_text = TXT['landing_sequence']['failures']
            chat = TXT['landing_sequence']['chat']

            is_low_on_fuel = seedship.fuel.get_ratio() < 0.3
            has_bad_terrain = AvailableLandscape.Terrain.Dangerous in seedship.planet.landscape
            is_planet_wide_ocean = seedship.planet.water == AvailableFeatures.Water.PlanetWideOcean
            time.sleep(2.8)
            # TODO cinematics

            # Confirmation
            looking_to_print_list.append(('chat', chat[:1]))

            cls.__run_print_list(looking_to_print_list, 1.0, 1.0)

            # Space phase
            looking_to_print_list.append(('phase', landing_sequence_text['space_phase']))
            looking_to_print_list.append(('chat', chat[1:]))
            if is_low_on_fuel:
                looking_to_print_list.append(('error', failure_text['space_phase']['low_fuel']))

            cls.__run_print_list(looking_to_print_list, 2.0, 4.0)
            # Atmosphere phase
            looking_to_print_list.append(('phase', landing_sequence_text['atmosphere_phase']))
            if is_low_on_fuel:
                looking_to_print_list.append(('error',
                                              failure_text['atmosphere_phase']['low_fuel']))

            cls.__run_print_list(looking_to_print_list, 2.0, 4.0)
            # Glide phase
            looking_to_print_list.append(('phase', landing_sequence_text['glide_phase']))
            if is_low_on_fuel:
                looking_to_print_list.append(('error',
                                             failure_text['glide_phase']['low_fuel']))

            if has_bad_terrain:
                looking_to_print_list.append(('error',
                                             failure_text['glide_phase']['bad_terrain']))

            if is_planet_wide_ocean:
                looking_to_print_list.append(('error',
                                             failure_text['glide_phase']['planet_wide_ocean']))

            cls.__run_print_list(looking_to_print_list, 2.5, 5.0)
            # touchdown phase
            looking_to_print_list.append(('phase', landing_sequence_text['touchdown_phase']))

            cls.__run_print_list(looking_to_print_list, 2.8, 5.0)
            time.sleep(4)

        @classmethod
        def __run_print_list(cls,
                             print_list: list,
                             delay_min: float = 0.1,
                             delay_max: float = 0.1):
            ''' Takes a list of lists of printables and
                prints randomically.
                format of print_list: [('chat', ['chat_message_a', 'chat_message_b'])]
            '''
            while print_list != []:
                print_type, print_sample = r.choice(print_list)
                if print_sample == []:
                    print_list.remove((print_type, print_sample))
                    continue
                to_print = print_sample.pop(0)
                cls.__print_landing_message(to_print, print_type)
                sleep_amount = r.random() * (delay_max - delay_min) + delay_min
                time.sleep(sleep_amount)

        @staticmethod
        def __print_landing_message(message: str, came_from: str):
            ''' prints one message from the landing sequence. '''
            if came_from == 'chat':
                print(f'{Color.WHITE}>>> {message}{Color.RESET}')
            elif message.startswith('[!]'):
                if came_from == 'phase':
                    print(f'{Color.YELLOW}{message}{Color.RESET}')
                else:
                    print(f'{Color.LIGHT_RED}{Color.BLINK}{message}{Color.RESET}')
            else:
                print(message)

    class Upgrade:
        command = translate_command('upgrade')
        argument_count = 1

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            scanners = {scanner.name.lower(): scanner
                        for scanner in seedship.scanners.values()}
            scanner_to_upgrade = splitted_line[1].lower()

            if scanner_to_upgrade not in scanners:
                raise SeedshipExecutionError('scanner_doesnt_exist')

            scanners[scanner_to_upgrade].upgrade()
            stats.modules_upgraded += 1

    class Help:
        command = translate_command('help')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            for text in TXT['help_text'].values():
                print(text)
                time.sleep(0.2)

    class Scan(PlanetRelatedCommand):
        command = translate_command('scan')
        argument_count = 0

        @classmethod
        def execute(cls, splitted_line, seedship, stats: GameStats) -> None:
            scan_result = seedship.scan_planet()
            stats.planets_scanned += 1
            cls.print_scan_result(scan_result)

    class Probe(PlanetRelatedCommand):
        command = translate_command('probe')
        argument_count = 0

        NO_LANDSCAPE = TXT['landscape']['no_landscape']

        @classmethod
        def execute(cls, splitted_line, seedship, stats: GameStats) -> None:
            scan_result = seedship.probe_planet()
            stats.planets_probed += 1
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
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            for shutdown_text in TXT['shutdown_sequence']:
                print(shutdown_text)
                time.sleep(0.15)
            enter_to_wake_up = translate_phrase('enter_to_wake_up')
            stats.sleeps_taken += 1
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
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            os.system('cls') if os.name == 'nt' else os.system('clear')

    class Idle:
        command = ''
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> None:
            pass

    class Exit:
        command = translate_command('exit')
        argument_count = 0

        @staticmethod
        def execute(splitted_line, seedship, stats: GameStats) -> bool:
            return True

    class Roll:
        command = translate_command('roll')
        argument_count = -1


        @classmethod
        def execute(cls, splitted_line, seedship, stats: GameStats) -> None:
            translated_sum = TXT['messages'].get('sum_die', 'Sum of die')
            for dice in DiceParser.get_dice(splitted_line):
                amount, faces = dice.amount, dice.faces
                sum_dice = 0
                print('-' * 10 + f' {amount}d{faces}:')
                for dice in range(1, amount + 1):
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

    all_classes = [Save, Load, Damage, Status, Upgrade, Help, Scan, Repair, Evade,
           Probe, Sleep, Clear, Waste, Idle, Land, Roll, Exit]
    all_commands = [c.command for c in all_classes]
    command_to_class = dict(zip(all_commands, all_classes))

    @classmethod
    def is_command(cls, command):
        return command in cls.all_commands


class ShowStats:
    @staticmethod
    def execute(seedship: Seedship, game_stats: GameStats):
        print()
        time.sleep(0.5)
        print(TXT['stats'].get('game_stats', '').center(80, ' '))
        print(f'+{"-" * 78}+')
        for message, value in game_stats.get_stats().items():
            time.sleep(0.3)
            print('+' + f'{TXT["stats"].get(message)}: {value}'.center(78, ' ') + '+')
            print(f'+{"-" * 78}+')
