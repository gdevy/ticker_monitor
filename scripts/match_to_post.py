import time

from utility_soup.iter import ForLoopTimer

from common.db import connect
from common.featurizers import counter, info
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

    posts = post_collection.find({}, limit=2)
    start = time.time()

    timer = ForLoopTimer()
    for post in timer(posts):
        results = iterate_comment_forest(reddit.submission(post['post_id']).comments,
                                         featurizers=[counter, info])
        if results:
            comment_collection.insert_many(results)

    print(timer)
