from settings import *
from time import sleep

class ShipStatus:

    def __init__(self):
        self.ship_status = {
            'colonistas': 1000,
            'sistemas': {
                'aterrissagem': 100,
                'construção': 100
            },
            'bancos de dados': {
                'científico': 100,
                'cultural': 100
            }
        }

    def print_status(self):
        for key, value in self.ship_status.items():
            if key == 'colonistas':
                self.__print_status_line(key, value, 0, False, False)
                sleep(0.2)
            else:
                print(key.title() + ':')
                for sub_key, sub_value in value.items():
                    self.__print_status_line(sub_key, sub_value, 4)
                    sleep(0.2)

    def damage_status(self, key, amount):
        status = self.ship_status
        a, b, c = status.get(key), status['sistemas'].get(key), status['bancos de dados'].get(key)

        if a is and b is None and c is None:
            raise NoSuchScanner(key + 'não é uma parte da nave!')

        amount = int(amount)


    # private

    @staticmethod
    def __print_status_line(key, value, tab_amount=0, add_percent=True, add_color=True):
        """
            Prints a seedship-style key-value pair.
            add_percent: add a % at the end of the value?
            tab_amount: add spacing before printing the pair?
            add_color: add color to value?
        """
        if value < 40:
            color = Color.LIGHT_RED
        elif value < 70:
            color = Color.YELLOW
        elif value < 95:
            color = Color.LIGHT_GREEN
        else:
            color = Color.GREEN
        str_left = Color.RESET + key.capitalize() + ': '
        str_right = color * add_color + str(value) + '%' * add_percent + Color.RESET
        string = str_left.ljust(18) + str_right.ljust(18)
        print(tab_amount * ' ' + string)


# Unit test
if __name__ == '__main__':
    a = ShipStatus()
    a.print_status()
