import os
import json

import requests

if __name__ == '__main__':
    from auth import get_auth

    token = get_auth()
    print(token)
    headers = {
        'Authorization': f'Bearer {token}',
        "User-Agent": f"ticker_monitor/0.1 by {os.environ['REDDIT_USERNAME']}",
    }

    url_stem = 'https://oauth.reddit.com'
    r = requests.get(f'{url_stem}/r/python/comments/o94ett', headers=headers)
    print(r.headers)
    print(r.json())

    with open("comments.json", 'w') as file:
        print(file.name)
        json.dump(r.json(), file, indent=4)
