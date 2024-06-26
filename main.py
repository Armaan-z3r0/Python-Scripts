import requests 
import argparse 
from tqdm import tqdm
from urllib.parse import urlparse

def ModURL(url):
    if not urlparse(url).scheme :
        url = 'http://' + url 
    if not url.endswith('/') :
        url = url + '/' 
    return url

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
    
def sendFuzz(modifiedURL,modifiedWORDLIST):
    count = 0
    for count,line in enumerate(tqdm(modifiedWORDLIST,desc="Progress" , unit="request")):
        try:
            res = requests.post(modifiedURL + line )
            statuscode = res.status_code
            count += 1 
            if statuscode != 404:
                tqdm.write(f"Success: {modifiedURL}{line} \t {statuscode}")
        except requests.exceptions.RequestException as e:
            tqdm.write(f"An error occurred with {modifiedURL}{line}: {e}")

parser = argparse.ArgumentParser("Take in the URL and Wordlist")

parser.add_argument('--url',type=str,required=True,help='needs a url')
parser.add_argument('--wordlist',type=str,required=True,help='needs a wordlists') 

args = parser.parse_args() 

unModifiedURL = args.url
unModifiedWordlist = args.wordlist

modifiedURL = ModURL(unModifiedURL)
modifiedWORDLIST = ModWORDLIST(unModifiedWordlist)

sendFuzz(modifiedURL,modifiedWORDLIST) 
