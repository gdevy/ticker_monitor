import os
import urllib
from datetime import datetime
from typing import List, Dict

import pymongo as pymongo
from pymongo.database import Database


class DBConnector:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DBConnector, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        import dotenv

        dotenv.load_dotenv()

        db_user = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
        db_pass = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])

        client = pymongo.MongoClient(
            f"mongodb+srv://{db_user}:{db_pass}@cluster0.audbf.mongodb.net/ticker_counter?retryWrites=true&w=majority")

        self.db = client.get_default_database()


db: Database = DBConnector().db


def get_posts(start: datetime) -> List[Dict]:
    found = db['post'].find({
        'posted_utc': [
            {'$gt': start},
        ]
    })

    return list(found)


indexes = {
    'feature': [
        [('name', pymongo.DESCENDING), ('version', pymongo.DESCENDING), ('comment_id', pymongo.DESCENDING), ],
    ],
    'post': [
        'post_id',
    ],
    'comment': [
        'comment_id',
    ]
}
