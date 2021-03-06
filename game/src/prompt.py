from .parser import Parser
from .language import TXT
from .util import SeedshipExecutionError
from .commands import AvailableCommands, ShowStats, DiceParser
from .game_stats import GameStats
from .seedship import SeedshipConsumable, Scanner, System, Database, Colonists
from .logger import Logger
import time
import readline
import atexit
import random


def translate_exception(exception):
    return TXT['error_messages'].get(exception, exception)


class Prompt:

    PROMPT_TEXT = 'sdshp> '
    HISTORY_FILE = 'log/command_history'

    @classmethod
    def show_menu(cls, seedship):
        pass

    @classmethod
    def serve_forever(cls, seedship):
        stats = GameStats()
        cls.__setup_save_at_exit(seedship, stats)

        cls.__setup_readline_history()
        readline.parse_and_bind('tab: complete')
        readline.set_completer(TabCompleter(seedship).complete)

        cls.__generate_and_log_seed()

        while True:
            try:
                line = input(cls.PROMPT_TEXT)
                parse_result = Parser.parse_line(line)
                if isinstance(parse_result, Parser.ParseFailure):
                    cls.__handle_parse_failure(parse_result)
                    continue
                # Load has special treatment. TODO rethink
                if parse_result.command == AvailableCommands.Load:
                    seedship, stats = parse_result.command.execute(parse_result.splitted_line, seedship, stats)
                    continue

                do_break = parse_result.command.execute(parse_result.splitted_line, seedship, stats)
                if do_break:
                    time.sleep(3)
                    ShowStats.execute(seedship, stats)
                    break
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                print()
                continue
            except SeedshipExecutionError as ex:
                cls.__handle_execution_failure(ex, parse_result.splitted_line)

    @classmethod
    def __handle_parse_failure(cls, parse_result: Parser.ParseFailure):
        exception_string = str(parse_result.exception)
        translated_exception = translate_exception(exception_string)
        if exception_string == 'incorrect_arg_count':
            expected, got = translate_exception('expected'), translate_exception('got')
            print(f'{translated_exception}: {expected} '
                  + f'{parse_result.command.argument_count}, '
                  + f'{got} {len(parse_result.splitted_line) - 1}')
            print(cls.__get_help_of_command(parse_result.command.command))

        elif exception_string == 'no_such_command':
            print(f'{translated_exception}: {parse_result.splitted_line[0]}')
            print(translate_exception('try_help'))

    @classmethod
    def __get_help_of_command(cls, command: str) -> str:
        return TXT['help_text'].get(command, command)

    @classmethod
    def __handle_execution_failure(cls, exception: Exception, splitted_line: list):
        exception_string = str(exception)
        translated_exception = translate_exception(exception_string)
        if len(splitted_line) < 1:
            return

        if isinstance(exception, DiceParser.RollException):
            print(f'{translated_exception}: {exception.dice}')
            return
        if exception_string == 'invalid_amount':
            if len(splitted_line) >= 2:
                print(f'{translated_exception}: {splitted_line[2]}')
            return
        print(f'{translated_exception}: {splitted_line[1]}')

    @classmethod
    def __setup_readline_history(cls):
        try:
            readline.read_history_file(cls.HISTORY_FILE)
            readline.set_history_length(100)
        except FileNotFoundError:
            pass

        atexit.register(readline.write_history_file, cls.HISTORY_FILE)

    @classmethod
    def __setup_save_at_exit(cls, seedship, game_stats):
        atexit.register(cls.__save_at_exit, seedship, game_stats)

    @classmethod
    def __save_at_exit(cls, seedship, game_stats):
        AvailableCommands.Save.execute([], seedship, game_stats)

    @staticmethod
    def __generate_and_log_seed():
        random_seed = random.randrange(2 ** 20)
        random.seed(random_seed)
        Logger.log_seed(random_seed)

class TabCompleter:
    def __init__(self, seedship):
        self.commands = AvailableCommands.all_commands
        self.modules = []
        for module_type in seedship.modules:
            for module in module_type.values():
                self.modules.append(module.name.lower())

        self.completers = []

    def __complete_command(self, text):
        return [command
                for command in self.commands
                if command.startswith(text)]

    def __complete_modules(self, text):
        return [module
                for module in self.modules
                if module.startswith(text)]

    def complete(self, text, state):
        if state == 0:
            lower_text = text.lower()
            commands = self.__complete_command(lower_text)
            modules = self.__complete_modules(lower_text)
            self.completers = commands + modules

        completers = self.completers

        if state >= len(completers):
            return None
        return completers[state]

if __name__ == '__main__':
    from seedship import Seedship
    s = Seedship()
    s.find_new_planet()
    Prompt.serve_forever(s)
