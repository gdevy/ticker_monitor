from datetime import datetime

import pandas as pd

from ..common.db import db


def get_feature_as_time_series(feature_name: str, start: datetime = None, end: datetime = None):
    query = {}

    if start:
        pass
    if end:
        pass

    comments = db['comments'].find(query)

    feature_series = db['feature'].find(
        {'comment_id': {'$in': [comment['comment_id'] for comment in comments]}})

    comments_df = pd.DataFrame(comments)
