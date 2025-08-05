
# This will check if the given url is UP or DOWN

# Custom
from decorator import log

from colorama import(
    Style,
    Fore
)
import requests

def checkURL(url):
    if not url.startswith(("http://", "https://")):
        url_https = "https://" + url
        url_http = "http://" + url

        if verifyURL(url_https):
            return
        else:
            verifyURL(url_http)
    else:
        verifyURL(url)


def verifyURL(url):
    try:
        response = requests.get(url, timeout=5)
        print(log.info(f"{Fore.BLUE}{url}{Style.RESET_ALL} us UP! : {response.status_code}"))
        return True
    except requests.ConnectionError:
        print(log.err(f"{Fore.BLUE}{url}{Style.RESET_ALL} is DOWN! (Connection Error)"))
    except requests.Timeout:
        print(log.err(f"{Fore.BLUE}{url}{Style.RESET_ALL} is DOWN! (Timeout)"))
    except requests.RequestException as e:
        print(log.err(f"{Fore.BLUE}{url}{Style.RESET_ALL} is DOWN! ({e})"))
    return False