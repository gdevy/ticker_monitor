import time

import tqdm

from common.db import connect
from common.featurizers import counter, text_analysis, info
from common.praw_interface import iterate_comment_forest, auth_praw

if __name__ == '__main__':
    import dotenv
    import logging

    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    reddit = auth_praw()
    db = connect()
    post_collection = db['post']
    comment_collection = db['comment']

    posts = post_collection.find({}, limit=1)
    start = time.time()

    for post in tqdm.tqdm(posts):
        results = iterate_comment_forest(reddit.submission(post['post_id']).comments,
                                         featurizers=[counter, text_analysis, info])

        comment_collection.insert_many(results)
