import logging
from typing import List, Dict
import requests
from datetime import datetime, timedelta

_submissions = r'https://api.pushshift.io/reddit/search/submission/'
_comments = r'https://api.pushshift.io/reddit/search/comments/'

logger = logging.getLogger(__name__)


def get_posts(subreddit: str, start: datetime, end: datetime) -> List[Dict]:
    response = requests.get(
        url=_submissions,
        params={
            'subreddit': subreddit,
            'before': int(end.timestamp()),
            'after': int(start.timestamp()),
            'limit': 100,
            'locked': 'false'

        }, )
    get_posts.request_count += 1

    logging.debug(f'request: {response.request.path_url}')

    response = response.json()

    logger.debug(f"returned: {len(response['data'])}")

    results = []
    for result in response['data']:
        results.append({
            'posted_utc': datetime.fromtimestamp(result['created_utc']),
            'post_id': result['id'],
            'url': result['permalink'],
            'title': result['title'],
            'subreddit': subreddit,
        })

    if len(results) == 100:
        rest = get_posts(subreddit, results[-1]['posted_utc'], end)
        results.extend(rest)

    return results


get_posts.request_count = 0

if __name__ == '__main__':
    posts = get_posts(
        'wallstreetbets',
        start=datetime.now() + timedelta(days=-30),
        end=datetime.now(),
    )
