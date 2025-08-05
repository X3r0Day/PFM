# XeroDay Automated Pentesting Framework

from colorama import (
    Style,
    Fore
)
import os, time, requests

# Custom
from checkUrl import checkURL
from decorator import log
from start import startFM

TARGET = None

intro = f'''

    {Fore.CYAN}{Style.BRIGHT}X3r0Day Framework v0.01
                        {Fore.GREEN}- By X3r0Day {Style.RESET_ALL}

'''

def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')
    return

def startScreen():
    print(f"{Fore.BLUE}Please select:")
    print("1. Subdomain discovery")
    print("2. All in one scan")

def mainScreen():
    print(f"{Fore.BLUE}Please select:")
    print("1. Create Profile (Comming Soon)")
    print("2. Select Profile (Comming Soon)")
    print("3. Select Target")
    print("4. Start")
    print("99. Exit")
    opt = input(f"{Style.RESET_ALL}{Style.BRIGHT}{Fore.YELLOW}> {Style.RESET_ALL}")
    clearScreen()
    return opt

def actionSelector():
    while True:
        selected = mainScreen()

        if selected == "1":
            print("Create Profile is comming soon...")
        elif selected == "2":
            print("Select Profile is comming soon...")
        elif selected == "3":
            global TARGET
            TARGET = input(f"Enter Target {Style.BRIGHT}(e.g, google.com){Fore.YELLOW}\n> {Style.RESET_ALL}")
            print(log.info(f"Selecting Target {Fore.CYAN}{TARGET}"))
            print(log.info(f"Checking if Target is up."))
            checkURL(TARGET)
        elif selected == "4":
            if TARGET:
                print("Starting..")
                time.sleep(.5)
                clearScreen()
                startFM(TARGET)
            else:
                print(log.err("Target Not selected!"))
            

        elif selected == "99":
            print("Exiting...")
            time.sleep(0.5)
            exit()
        else:
            continue


def main():
    print(intro)
    time.sleep(1)
    clearScreen()
    actionSelector()

if __name__ == "__main__":
    main()