from src.parser import Parser
from src.language import TXT
from src.util import SeedshipExecutionError
from src.commands import AvailableCommands
from src.game_status import GameStatus


def translate_exception(exception):
    return TXT['error_messages'].get(exception, exception)


class Prompt:

    PROMPT_TEXT = 'sdshp> '

    @classmethod
    def show_menu(cls, seedship):
        pass

    @classmethod
    def serve_forever(cls, seedship):
        status = GameStatus()
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
                    cls.show_final_stats(status)
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
    def show_final_stats(cls, final_stats: GameStatus):
        pass

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


if __name__ == '__main__':
    from seedship import Seedship
    s = Seedship()
    s.find_new_planet()
    Prompt.serve_forever(s)
