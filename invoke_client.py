import os
import time
import requests
from requests.auth import HTTPBasicAuth



SUCCESS_INTERVAL=120
FAIL_INTERVAL=1200

#TOKEN_URL=os.getenv("TOKEN_URL")

TOKEN_URL=os.getenv("TOKEN_URL")
INVOKE_URL=os.getenv("INVOKE_URL")
USERNAME=os.getenv("SMARTWEB_USER")
PASSWORD=os.getenv("SMARTWEB_PASSWORD")

# Define headers as seen in the browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Connection': 'keep-alive'
    # Add other headers if needed
}


SUCCESS_FLAG="updated"

def onSuccess():
    print("success")
    time.sleep(SUCCESS_INTERVAL)

def onFail():
    print("fail")
    time.sleep(FAIL_INTERVAL)


def get_token()->str:
    ret = ""
    try:        
        response = requests.get(TOKEN_URL, headers=headers, auth=HTTPBasicAuth(USERNAME, PASSWORD))

        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        ret = response.text
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")   
    return ret

def invoke_update(token:str)->bool:
    headers = {
        'token':'{}'.format(token)
    }
    ret = False
    try:
        response = requests.get(INVOKE_URL, headers=headers  )
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx and 5xx)
        if(response.text.find(SUCCESS_FLAG) != -1):
            ret = True
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")    
    return ret

def main():
    err_found = False
    while True:       
        err_found = True
        token = get_token()       
        if not token=="" and invoke_update(token):
            err_found = False
        elif not token=="" and err_found and invoke_update(token):
            err_found = False

        if err_found:
            onFail()
        else:
            onSuccess()
        

if __name__ == "__main__":
    main()