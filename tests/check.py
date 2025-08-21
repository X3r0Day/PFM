import json
import threading
import subprocess
from pathlib import Path
from decorator import log
import time
import os

from colorama import (
    Style,
    Fore
)

# Scanning modules


# Hardcoding profile for now
profile = 'profile1.json'

def loadProf(target):
    profile_path = Path(__file__).parent.parent / 'profile' / profile
    with open(profile_path) as f:
        data = json.load(f)
        startProf(data, target)

def runTool(name, command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )
        print(f"\n-- Output From {name} -- ")
        print(result.stdout)
        if result.stderr:
            print(f"{name} stderr: {result.stderr}")
    except Exception as e:
        print(f"[{name} error]: {e}")

def startProf(data, target):
    # 1st Group
    subprocess.run("mkdir -p output", shell=True) # Initializing output directory
    firstThread = []

    if data["RUN"]["nmapscan"]["enabled"] == "True":
        print("Running NMAP")
        scanType = data["RUN"]["nmapscan"]["scantype"]
        t = threading.Thread(target=runTool, args=("NMAP", f"{scanType} {target} | tee output/nmapscan.scan"))
        firstThread.append(t)
        t.start()

    if data["RUN"].get("subfinder") == "True":
        print("Running Subfinder")
        t = threading.Thread(target=runTool, args=("Subfinder", f"subfinder -d {target} -silent | tee output/subfinder.txt"))
        firstThread.append(t)
        t.start()

    if data["RUN"].get("assetfinder") == "True":
        print("Running Assetfinder")
        t = threading.Thread(target=runTool, args=("Assetfinder", f"assetfinder -subs-only {target} | tee output/assetfinder.txt"))
        firstThread.append(t)
        t.start()


    # Wait for 1st group to finish
    for t in firstThread:
        t.join()

    # Filtering and httpx probing
    log.suc("Scan Completed! Filtering out garbage.")
    time.sleep(1)
    os.system("clear")
    subprocess.run("cat output/*.txt | sort -u  > output/filtered.txt", shell=True)

    log.info("Garbage filtered out! Created 'output/filtered.txt'!"); time.sleep(1)
    log.info("Cleaning up...")
    log.info(f"Deleting {Style.BRIGHT} assetfinder.txt, subfinder.txt")
    subprocess.run("rm output/assetfinder.txt output/subfinder.txt", shell=True)

    log.info("Filtering alive subdomains.")

    # httpx config
    httpx = data["RUN"]["httpx"]
    ports = httpx["ports"]
    threadcnt = httpx["threadcnt"]
    command = httpx["command"]

    subprocess.run(f"cat output/filtered.txt | httpx-pd -ports {ports} -threads {threadcnt} > output/alivesubs.txt", shell=True)
    log.info(f"Filtered results saved to '{Style.BRIGHT}output/alivesubs.txt{Style.NORMAL}'")

    '''
    Standalone commands
    '''
    os.system("clear")
    log.info(f"Runnig {Style.BRIGHT}{Fore.BLUE}katana{Style.RESET_ALL} scan")
    time.sleep(1)
    
    # Katana config
    depth = data["RUN"]["katana"]["depth"]
    subprocess.run(f"katana -u output/alivesubs.txt -d {depth} -o output/urls.txt", shell=True)
    log.info("Saved results to output/urls.txt!\n\n")
    time.sleep(2)

    # Filter config
    n = data["UrlFilter"]["entries"]
    filters = data["UrlFilter"]
    
    for i in range(1, n+1):
        pattern = filters[str(i)]
        output = f"output{i}.txt"
        subprocess.run(f"cat output/urls.txt | grep -E '{pattern}' | urldedupe | tee output/output{i}.txt", shell=True)
        log.info(f"Saved results to output/output{i}.txt")
    subprocess.run("cat output/*.txt | sort -u  > output/filteredOutput.txt", shell=True)
    log.info("Filtered urls!")


    # 2nd Group
    secondThread = []
    
