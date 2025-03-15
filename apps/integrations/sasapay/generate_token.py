
import requests
import json
from requests.auth import HTTPBasicAuth

SASAPAY_CLIENT_ID = "Eb62EFOsnLc9ARkrp9cFCj5CQAgXGqY3SSQOTxUC"
SASAPAY_CLIENT_SECRET = "h5Ef0CsZKWYenftCnY6NZqoKvqPhqtdZ59GDzdZ5tPYmsLy9kquXwqdECdb5CN6aA1HfQRds32al7vq1UjRSiq2dCnltDMw5eVjjgd3fyjTNZRwwuJmYmedup0IboZ5L"

def token():
    url = 'https://sandbox.sasapay.app/api/v1/auth/token/?grant_type=client_credentials'
    params = {'grant_type': 'client_credentials'}
    res = requests.get(url,
                        auth=HTTPBasicAuth(SASAPAY_CLIENT_ID, SASAPAY_CLIENT_SECRET), params=params)
    response = json.loads(res.text)
    access_token = response['access_token']
    print(access_token)


token()