import os

TERMINAL_SIZE_SET = False
DEFAULT_TERMINAL_SIZE = (80, 25)
TERMINAL_SIZE = DEFAULT_TERMINAL_SIZE

class Color:
    BLACK =        '\033[0;30m'
    GRAY =         '\033[1;30m'
    RED =          '\033[0;31m'
    LIGHT_RED =    '\033[1;31m'
    GREEN =        '\033[0;32m'
    LIGHT_GREEN =  '\033[1;32m'
    BROWN =        '\033[0;33m'
    YELLOW =       '\033[1;33m'
    BLUE =         '\033[0;34m'
    LIGHT_BLUE =   '\033[1;34m'
    PURPLE =       '\033[0;35m'
    LIGHT_PURPLE = '\033[1;35m'
    CYAN =         '\033[0;36m'
    LIGHT_CYAN =   '\033[1;36m'
    LIGHT_GRAY =   '\033[0;37m'
    WHITE =        '\033[1;37m'
    BLINK =        '\033[5m'
    RESET =        '\033[0m'


class SeedshipExecutionError(Exception):
    pass

if os.name == 'nt':
    clear_screen = lambda: os.system('cls')
else:
    clear_screen = lambda: os.system('clear')

def get_screen_size() -> (int, int):
    global TERMINAL_SIZE, TERMINAL_SIZE_SET
    if TERMINAL_SIZE_SET:
        return TERMINAL_SIZE
    if os.name == 'nt':
        TERMINAL_SIZE = __get_screen_size_windows() 
    else: 
        TERMINAL_SIZE = __get_screen_size_unix()
    TERMINAL_SIZE_SET = True
    return TERMINAL_SIZE

def __get_screen_size_unix() -> (int, int):
    import subprocess
    return tuple(map(int, subprocess.check_output(['stty', 'size']).split()))

def __get_screen_size_windows() -> (int, int):
    # https://gist.github.com/jtriley/1108174
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        h = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
        if res:
            (bufx, bufy, curx, cury, wattr,
             left, top, right, bottom,
             maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
            sizex = right - left + 1
            sizey = bottom - top + 1
            return sizex, sizey
    except:
        return DEFAULT_TERMINAL_SIZE