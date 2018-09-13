from parser import Parser
from language import TXT
from util import SeedshipExecutionError
from commands import AvailableCommands


def translate_exception(exception):
    return TXT['error_messages'].get(exception, exception)


class Prompt:

    PROMPT_TEXT = 'sdshp> '

    @classmethod
    def show_menu(cls, seedship):
        pass

    @classmethod
    def serve_forever(cls, seedship):
        while True:
            try:
                line = input(cls.PROMPT_TEXT)
                parse_result = Parser.parse_line(line)
                if isinstance(parse_result, Parser.ParseFailure):
                    cls.__handle_parse_failure(parse_result)
                    continue
                do_break = parse_result.command.execute(parse_result.splitted_line, seedship)
                if do_break:
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

        elif exception_string == 'no_such_command':
            print(f'{translated_exception}: {parse_result.splitted_line[0]}')
            print(translate_exception('try_help'))

    @classmethod
    def __handle_execution_failure(cls, exception: Exception, splitted_line: list):
        exception_string = str(exception)
        translated_exception = translate_exception(exception_string)
        if len(splitted_line) < 1:
            return

        if isinstance(exception, AvailableCommands.Roll.RollException):
            print(f'{translated_exception}: {exception.dice}')
            return
        print(f'{translated_exception}: {splitted_line[1]}')


if __name__ == '__main__':
    from seedship import Seedship
    s = Seedship()
    s.find_new_planet()
    Prompt.serve_forever(s)
