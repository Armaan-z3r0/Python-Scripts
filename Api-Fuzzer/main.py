import requests
import argparse
import pyfiglet
from tabulate import tabulate
from tqdm import tqdm
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def ModURL(url):
    if not urlparse(url).scheme:
        url = 'http://' + url
    if not url.endswith('/'):
        url = url + '/'
    return url

def Draw():
    print("=" * 50)
    result = pyfiglet.figlet_format("FuzzBuzz", font="slant")
    print(result, end="")
    print("=" * 50)

def ModWORDLIST(unModifiedWordlist):
    try:
        with open(unModifiedWordlist, 'r') as file:
            lines = file.readlines()
            concatenated_string = [line.strip() for line in lines]
            return concatenated_string
    except FileNotFoundError:
        print(f"\nThe file {unModifiedWordlist} was not found.")
        return -1
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1

def send_request(url):
    try:
        res = requests.post(url)
        statuscode = res.status_code
        if statuscode != 404:
            return {"URL": url, "Status Code": statuscode}
    except requests.exceptions.RequestException as e:
        return {"URL": url, "Status Code": f"Error: {e}"}
    return None

def sendFuzz(modifiedURL, modifiedWORDLIST, max_workers=10):
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(send_request, modifiedURL + line): line for line in modifiedWORDLIST}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Progress", unit="request"):
            result = future.result()
            if result and result["Status Code"] == 200:
                results.append(result)
                print("\033c", end="")  # Clear the terminal
                Draw()
                print(tabulate(results, headers="keys", tablefmt="pretty"))

if __name__ == "__main__":
    Draw()

    parser = argparse.ArgumentParser(description="Take in the URL and Wordlist")
    parser.add_argument('--url', type=str, required=True, help='URL to fuzz')
    parser.add_argument('--wordlist', type=str, required=True, help='Path to the wordlist')

    args = parser.parse_args()

    unModifiedURL = args.url
    unModifiedWordlist = args.wordlist

    modifiedURL = ModURL(unModifiedURL)
    modifiedWORDLIST = ModWORDLIST(unModifiedWordlist)

    if modifiedWORDLIST != -1:
        sendFuzz(modifiedURL, modifiedWORDLIST)
