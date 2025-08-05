import json
import threading
import subprocess
from pathlib import Path
from decorator import log

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
    threads = []

    if data["RUN"]["nmapscan"]["enabled"] == "True":
        print("Running NMAP")
        scanType = data["RUN"]["nmapscan"]["scantype"]
        t = threading.Thread(target=runTool, args=("NMAP", f"{scanType} {target} | tee nmapscan.txt"))
        threads.append(t)
        t.start()

    if data["RUN"].get("subfinder") == "True":
        print("Running Subfinder")
        t = threading.Thread(target=runTool, args=("Subfinder", f"subfinder -d {target} -silent | tee subfinder.txt"))
        threads.append(t)
        t.start()

    if data["RUN"].get("assetfinder") == "True":
        print("Running Assetfinder")
        t = threading.Thread(target=runTool, args=("Assetfinder", f"assetfinder -subs-only {target} | tee assetfinder.txt"))
        threads.append(t)
        t.start()

    # Wait for all tools to finish
    for t in threads:
        t.join()
        log.suc("Scan Completed!")