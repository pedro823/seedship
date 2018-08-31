from language import TXT
from util import Color


def translate_command(command):
    return TXT['command'].get(command, command)


class AvailableCommands:
    class Damage:
        command = translate_command('damage')
        argument_count = 2

        @staticmethod
        def execute(splitted_line, seedship):
            module_to_damage = splitted_line[1].lower()
            translated_modules = {}

            for module_list in [seedship.scanners, seedship.databases, seedship.systems]:
                for module in module_list.values():
                    translated_modules[module.name.lower()] = module

            if module_to_damage not in translated_modules:
                raise Exception(f'module={splitted_line[1]} doesn\'t exist')

            amount = int(splitted_line[2])
            translated_modules[module_to_damage].damage(amount)

    class Status:
        command = translate_command('status')
        argument_count = 0

        @classmethod
        def execute(cls, splitted_line, seedship):
            pass

    class Upgrade:
        command = translate_command('upgrade')
        argument_count = 1

    class Help:
        command = translate_command('help')
        argument_count = 0

    class Scan:
        command = translate_command('scan')
        argument_count = 0

    class Probe:
        command = translate_command('probe')
        argument_count = 0

    class Sleep:
        command = translate_command('sleep')
        argument_count = 0

    all = [Damage, Status, Upgrade, Help, Scan, Probe, Sleep]
    all_commands = [c.command for c in all]
    command_to_class = dict((name, command) for name, command in zip(all_commands, all))

    @classmethod
    def is_command(cls, command):
        return command in cls.all_commands
