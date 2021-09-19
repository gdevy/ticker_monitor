import logging
from datetime import datetime, timedelta

from pymongo.collection import Collection

from common.db import db
from common.push_shift_interface import get_posts

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import dotenv

    dotenv.load_dotenv()

    posts = get_posts('wallstreetbets',
                      end=datetime.now(),
                      start=datetime.now() - timedelta(hours=1))

    post_collection: Collection = db['post']

    inserted = post_collection.insert_many(posts)
    print(len(inserted.inserted_ids))
