from parser import Parser
from language import TXT


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
                parse_result.command.execute(parse_result.splitted_line, seedship)
            except EOFError:
                print()
                break
            except KeyboardInterrupt:
                continue

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
            print(f'{translated_exception}: {parse_result.command_line}')


if __name__ == '__main__':
    from seedship import Seedship
    s = Seedship()
    s.find_new_planet()
    Prompt.serve_forever(s)
