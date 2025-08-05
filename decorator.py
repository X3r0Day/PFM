from colorama import Style, Fore

class log:
    @staticmethod
    def suc(msg): return f"{Style.BRIGHT}{Fore.GREEN}[+] {Style.RESET_ALL}{msg}"

    @staticmethod
    def warn(msg): return f"{Fore.YELLOW}[-] {Style.RESET_ALL}{msg}"

    @staticmethod
    def err(msg): return f"{Style.BRIGHT}{Fore.RED}[x] {Style.RESET_ALL}{msg}"

    @staticmethod
    def info(msg): return f"{Fore.BLUE}[!] {Style.RESET_ALL}{msg}"