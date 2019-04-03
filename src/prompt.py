from src.parser import Parser
from src.language import TXT
from src.util import SeedshipExecutionError
from src.commands import AvailableCommands, ShowStats
from src.game_stats import GameStats
from src.seedship import SeedshipConsumable, Scanner, System, Database, Colonists
import time
import readline
import atexit


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
        status = GameStats()
        cls.__setup_readline_history()
        readline.parse_and_bind('tab: complete')
        readline.set_completer(TabCompleter.complete)
        while True:
            try:
                line = input(cls.PROMPT_TEXT)
                parse_result = Parser.parse_line(line)
                if isinstance(parse_result, Parser.ParseFailure):
                    cls.__handle_parse_failure(parse_result)
                    continue
                # Load has special treatment. TODO rethink
                if parse_result.command == AvailableCommands.Load:
                    seedship, status = parse_result.command.execute(parse_result.splitted_line, seedship, status)
                    continue

                do_break = parse_result.command.execute(parse_result.splitted_line, seedship, status)
                if do_break:
                    time.sleep(3)
                    ShowStats.execute(seedship, status)
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

        if isinstance(exception, AvailableCommands.Roll.RollException):
            print(f'{translated_exception}: {exception.dice}')
            return
        if exception_string == 'invalid_amount':
            if len(splitted_line) < 2:
                return
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


class TabCompleter:

    COMMANDS = AvailableCommands.all_commands
    MODULE_NAMES = tuple(i.name for i in (SeedshipConsumable, Scanner, System, Database, Colonists))
    completers = []

    @classmethod
    def __complete_command(cls, text):
        return [command
                for command in cls.COMMANDS
                if command.startswith(text)]

    @classmethod
    def __complete_modules(cls, text):
        return [module
                for module in cls.MODULE_NAMES
                if module.startswith(text)]

    @classmethod
    def complete(cls, text, state):
        if state == 0:
            commands = cls.__complete_command(text)
            modules = cls.__complete_modules(text)
            cls.completers = commands + modules

        completers = cls.completers

        if state >= len(completers):
            return None
        return completers[state]

if __name__ == '__main__':
    from seedship import Seedship
    s = Seedship()
    s.find_new_planet()
    Prompt.serve_forever(s)
