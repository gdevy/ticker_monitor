import logging
from datetime import datetime, timedelta

from tqdm import tqdm

from pymongo.collection import Collection

from ticker_monitor.common.db import db
from ticker_monitor.common.push_shift_interface import get_posts

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    import dotenv

    dotenv.load_dotenv()

    for day_offset in tqdm(range(14)):
        start = datetime.now() - timedelta(days=14)

        posts = get_posts('wallstreetbets',
                          end=start + timedelta(days=day_offset + 1),
                          start=start + timedelta(days=day_offset))

        post_collection: Collection = db['post']

        inserted = post_collection.insert_many(posts)
        print(len(inserted.inserted_ids))
