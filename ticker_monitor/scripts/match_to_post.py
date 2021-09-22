import time

from tqdm import tqdm
from utility_soup.iter import ForLoopTimer

from ticker_monitor.common.db import db
from ticker_monitor.common.featurizers import counter, extract_features
from ticker_monitor.common.praw_interface import iterate_comment_forest, auth_praw

if __name__ == '__main__':
    import dotenv
    import logging

    clear_db = True
    # if clear_db:
    #     db.drop_collection('comment')

    featurizers = [counter, ]

    dotenv.load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    reddit = auth_praw()
    post_collection = db['post']
    comment_collection = db['comment']
    feature_collection = db['feature']

    posts = post_collection.find({})
    start = time.time()

    timer = ForLoopTimer()
    for post in timer(tqdm(posts)):
        comments = iterate_comment_forest(reddit.submission(post['post_id']).comments)

        if comments:
            comment_collection.insert_many([comment[1] for comment in comments])

        for comment, comment_info in comments:
            features = extract_features(comment, comment.submission, comment_info['depth'], featurizers=featurizers)
            feature_collection.insert_many(features)

    print(timer)
