import datetime
import logging
import os
import json

import requests
from requests.auth import HTTPBasicAuth

logger = logging.getLogger(__name__)


def get_auth(force_refresh=False):
    token_cache_file = 'token.json'
    if not force_refresh:
        with open(token_cache_file, 'r') as file:
            last_token = json.load(file)
            issued_at = datetime.datetime.fromisoformat(last_token['issued_at'])
            print(f"Last token issued at: {issued_at.time()} (on {str(datetime.date)})")
            if issued_at + datetime.timedelta(0, last_token['expires_in']) > datetime.datetime.now():
                return last_token['access_token']

    client_auth = HTTPBasicAuth(os.environ['REDDIT_APP_ID'], os.environ['REDDIT_APP_SECRET'])
    post_data = {"grant_type": "password",
                 "username": os.environ['REDDIT_USERNAME'],
                 "password": os.environ['REDDIT_PASSWORD'],
                 "scope": "*"}
    headers = {"User-Agent": f"ticker_monitor/0.1 by {os.environ['REDDIT_USERNAME']}"}
    response = requests.post("https://www.reddit.com/api/v1/access_token",
                             auth=client_auth,
                             data=post_data,
                             headers=headers)

    current_token = {
        'issued_at': str(datetime.datetime.now()),
        'expires_in': response.json()['expires_in'],
        'access_token': response.json()['access_token'],
    }

    with open(token_cache_file, 'w') as file:
        json.dump(current_token, file, indent=4)
    return response.json()['access_token']
