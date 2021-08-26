import os
import urllib

import pymongo as pymongo
from pymongo.database import Database


def connect() -> Database:
    db_user = urllib.parse.quote_plus(os.environ['MONGODB_USER'])
    db_pass = urllib.parse.quote_plus(os.environ['MONGODB_PASSWORD'])

    client = pymongo.MongoClient(
        f"mongodb+srv://{db_user}:{db_pass}@cluster0.audbf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

    return client['ticker_counter']
