from colorama import Style, Fore

class log:
    @staticmethod
    def suc(msg):  print(f"{Style.BRIGHT}{Fore.GREEN}[+] {Style.RESET_ALL}{msg}")

    @staticmethod
    def warn(msg): print(f"{Fore.YELLOW}[-] {Style.RESET_ALL}{msg}")

    @staticmethod
    def err(msg):  print(f"{Style.BRIGHT}{Fore.RED}[x] {Style.RESET_ALL}{msg}")

    @staticmethod
    def info(msg): print(f"{Fore.BLUE}[!] {Style.RESET_ALL}{msg}")