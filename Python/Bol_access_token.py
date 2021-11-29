import requests
from requests.auth import HTTPBasicAuth
import json


def get_token():
    url = "https://login.bol.com/token?grant_type=client_credentials"

    payload={}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, auth = HTTPBasicAuth('5f6e61cd-9e59-4728-8549-f9ad4132b9dd', 'Hr6ldvMG4CQv2sg3nWQPbub9l2D-zbX0CuxGUqUeHy-E-iuzjcGQyvlU1sERcHOd_6DXwlZDmZqsyItQXCL2Rg'))

    response_dict = json.loads(response.text)
    return response_dict['access_token']


if __name__ == "__main__":
    get_token()