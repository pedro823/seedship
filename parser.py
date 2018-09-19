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
        def __init__(self, exception: Exception,
                     splitted_line: list,
                     command=None):
            self.exception = exception
            self.splitted_line = splitted_line
            self.command = command

    @classmethod
    def parse_line(cls, command_line: str) -> ParseResult:
        ''' Returns parsed input from user '''
        try:
            splitted_line = cls.__split_line(command_line)
            if splitted_line == []:
                return cls.ParseSuccess(AvailableCommands.Idle,
                                        splitted_line)
            command = splitted_line[0]
            if not AvailableCommands.is_command(command):
                return cls.ParseFailure(exception=Exception('no_such_command'),
                                        splitted_line=splitted_line)

            if not cls.__check_argument_amount(splitted_line):
                return cls.ParseFailure(exception=Exception('incorrect_arg_count'),
                                        splitted_line=splitted_line,
                                        command=AvailableCommands.command_to_class[command])

            return cls.ParseSuccess(AvailableCommands.command_to_class[command],
                                    splitted_line)
        except Exception as ex:
            return cls.ParseFailure(exception=ex, splitted_line=splitted_line)

    @classmethod
    def __split_line(cls, command_line):
        ''' Splits line into separate words '''
        # TODO:30 allow this to have quotes
        return [command.strip().lower() for command in command_line.strip().split()]

    @classmethod
    def __check_argument_amount(cls, splitted_line):
        ''' Checks if the correct amount of arguments was given to a command '''
        command = splitted_line[0]
        command_class = AvailableCommands.command_to_class[command]
        if command_class.argument_count == -1:
            # variable arglength
            return True
        return len(splitted_line) - 1 == command_class.argument_count


if __name__ == '__main__':
    from seedship import Seedship
    sdshp = Seedship()

    parse_result = Parser.parse_line('help')
    parse_result.command.execute(parse_result.splitted_line, sdshp)
