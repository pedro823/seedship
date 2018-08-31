from commands import AvailableCommands
from language import TXT


def translate_error(error):
    ''' Returns the translation of the error message. '''
    return TXT['error'].get(error)


class Parser:

    class ParseResult:
        pass

    class ParseSuccess(ParseResult):
        def __init__(self, command, splitted_line):
            self.command = command
            self.splitted_line = splitted_line

    class ParseFailure(ParseResult):
        def __init__(self, message='', exception=None):
            self.exception = exception
            if message:
                self.message = message
            else:
                self.message = str(self.exception) if exception else ''

    @classmethod
    def parse_line(cls, command_line: str) -> ParseResult:
        ''' Returns parsed input from user '''
        try:
            splitted_line = cls.__split_line(command_line)
            command = splitted_line[0]
            if not AvailableCommands.is_command(command):
                return cls.ParseFailure(message=translate_error('no_such_command'))
            if not cls.__check_argument_amount(splitted_line):
                return cls.ParseFailure(message=translate_error('incorrect_arg_amount'))
            return cls.ParseSuccess(AvailableCommands.command_to_class[command],
                                    splitted_line)
        except Exception as ex:
            return cls.ParseFailure(exception=ex)

    @classmethod
    def __split_line(cls, command_line):
        ''' Splits line into separate words '''
        # TODO allow this to have quotes
        return [command.strip() for command in command_line.strip().split()]

    @classmethod
    def __check_argument_amount(cls, splitted_line):
        ''' Checks if the correct amount of arguments was given to a command '''
        command = splitted_line[0]
        command_class = AvailableCommands.command_to_class[command]
        return len(splitted_line) - 1 == command_class.argument_count


if __name__ == '__main__':
    from seedship import Seedship
    sdshp = Seedship()

    print(sdshp.scanners['atmosphere'].health)
    parse_result = Parser.parse_line('damage atmosfera 5')
    parse_result.command.execute(parse_result.splitted_line, sdshp)
    print(sdshp.scanners['atmosphere'].health)
