from colorama import init as c_init
from colorama import Fore, Style


class Utility(object):
    def __init__(self):
        c_init(autoreset=True)
        return None

    def print_error_message(self, message):
        print(Fore.RED + Style.BRIGHT + message)
        return

    def print_informational_message(self, message):
        print(Fore.GREEN + message)
        return

    def print_debug_message(self, message):
        print(Fore.BLUE + Style.NORMAL + message)
        return

    def print_halo_status_message(self, message):
        print(Fore.BLUE + Style.BRIGHT + message)
        return

    def print_aws_status_message(self, message):
        print(Fore.YELLOW + Style.BRIGHT + message)
        return

    @classmethod
    def string_from_file(cls, filepath):
        retval = ""
        with open(filepath, 'r') as f_obj:
            retval = f_obj.read()
        return retval
