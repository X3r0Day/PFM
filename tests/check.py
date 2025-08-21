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
    subprocess.run("mkdir -p output/temp", shell=True) # Initializing output directory
    firstThread = []

    if data["RUN"]["nmapscan"]["enabled"] == "True": # NMAP SCAN
        print("Running NMAP")
        scanType = data["RUN"]["nmapscan"]["scantype"]
        t = threading.Thread(target=runTool, args=("NMAP", f"{scanType} {target} | tee output/temp/nmapscan.scan"))
        firstThread.append(t)
        t.start()

    if data["RUN"].get("subfinder") == "True": # SUBFINDER SCAN
        print("Running Subfinder")
        t = threading.Thread(target=runTool, args=("Subfinder", f"subfinder -d {target} -silent | tee output/temp/subfinder.txt"))
        firstThread.append(t)
        t.start()

    if data["RUN"].get("assetfinder") == "True": # ASSETFINDER SCAN
        print("Running Assetfinder")
        t = threading.Thread(target=runTool, args=("Assetfinder", f"assetfinder -subs-only {target} | tee output/temp/assetfinder.txt"))
        firstThread.append(t)
        t.start()


    # Wait for 1st group to finish
    for t in firstThread:
        t.join()

    # Filtering and httpx probing
    log.suc("Scan Completed! Filtering out garbage.")
    time.sleep(1)
    os.system("clear")

    # ---------------------------------- SORTING DISCOVERED SUBDOMAINS ---------------------------------- #
    subprocess.run(
        "sort -u output/temp/*.txt -o output/subs.txt",
        shell=True
    )
    log.info("Garbage filtered out! Created 'output/subs.txt'!")
    time.sleep(1)

    # ---------------------------------- CLEANING UP SUBDOMAINS STANDALONE TXT ---------------------------------- #
    log.info("Cleaning up assetfinder.txt, subfinder.txt")
    subprocess.run("rm -f output/temp/assetfinder.txt output/temp/subfinder.txt", shell=True)

    # ---------------------------------- FILTERING LIVE SUBDOMAINS ---------------------------------- #
    httpx = data["RUN"]["httpx"]
    ports = httpx["ports"]
    threads = httpx["threadcnt"]

    subprocess.run(
        f"httpx-pd -l output/subs.txt -ports {ports} -threads {threads} > output/live.txt && rm subs.txt",
        shell=True
    )
    log.info("Filtered results saved to 'output/live.txt'")

    # ---------------------------------- CRAWLING URLS USING KATANA ---------------------------------- #
    depth = data["RUN"]["katana"]["depth"]
    subprocess.run(
        f"katana -u output/live.txt -d {depth} -o output/urls.txt",
        shell=True
    )
    log.info("Saved results to output/urls.txt!")

    # ---------------------------------- FILTERING URLS ---------------------------------- #
    subprocess.run(
        '''grep -E "\?.+=" output/urls.txt | tee output/sqli.txt''',
        shell=True
    )
    log.info("Filtered SQLi URLs saved to output/sqli.txt")

    # ---------------------------------- SORT UNIQUE ---------------------------------- #
    # subprocess.run(
    #    "sort -u output/sqli.txt -o output/sqli.txt",
    #    shell=True
    #)
    #log.info("Final sorted SQLi URLs saved to output/sqli.txt")


    # 2nd Group
    secondThread = []