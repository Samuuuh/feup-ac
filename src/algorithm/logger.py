from colorama import Fore, Style


class Logger:

    @staticmethod
    def print_err(msg: str):
        print(f"{Fore.RED}[ ERRO ] {msg} {Style.RESET_ALL}")

    @staticmethod
    def print_suc(msg: str):
        print(f"{Fore.GREEN}[ SUCC ] {msg} {Style.RESET_ALL}")

    @staticmethod
    def print_wrn(msg: str):
        print(f"{Fore.YELLOW}[ WARN ] {msg} {Style.RESET_ALL}")

    @staticmethod
    def print_info(msg: str):
        print(f"{Fore.CYAN}[ INFO ] {msg} {Style.RESET_ALL}")
