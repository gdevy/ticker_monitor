import logging
from datetime import datetime, timedelta

from pymongo.collection import Collection

from common.db import connect
from common.push_shift_interface import get_posts

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import dotenv

    dotenv.load_dotenv()

    posts = get_posts('wallstreetbets',
                      end=datetime.now(),
                      start=datetime.now() - timedelta(days=30))

    db: Collection = connect()['post']

    inserted = db.insert_many(posts)
    print(len(inserted.inserted_ids))
