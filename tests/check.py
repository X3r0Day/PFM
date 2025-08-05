import json
import sys
from pathlib import Path

# Custom modules
from tests.scan import scanTarget

# sys.path.append(str(Path(__file__).parent.parent))

profile = 'profile1.json' # Hardcoding profile1.json for now, later I will make it through userinput

def loadProf(target):
    with open(Path(__file__).parent.parent / 'profile' / profile) as f:
        data = json.load(f)
        startProf(data, target)


def startProf(data, target):
    if data["RUN"]["nmap"] == "True": # Checking NMAP
        print("Running NMAP")
        scanTarget(target)
    
    if data["RUN"]["subfinder"] == "True": # Checking subfinder
        print("Running subfinder")

    if data["RUN"]["assetfinder"] == "True": # Checking assetfinder
        print("Running assetfinder")


        