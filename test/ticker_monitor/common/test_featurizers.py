from typing import Tuple

import pytest
from praw.reddit import Comment

from ticker_monitor.common.featurizers import counter, tickers


def test_extract_features():
    assert True


@pytest.mark.parametrize(
    'comment_id, non_zero_tickers, freqs',
    [
        ('hdqygye', ('bb',), (1,),),
        ('hdqygye', ('bb',), (1,),),
    ]
)
def test_counter(praw_conn, comment_id, non_zero_tickers, freqs):
    comment = praw_conn.comment(comment_id)

    feature = counter(comment, comment.submission, 1)
    ticker_idx, ticker_names = zip(*[(tickers.index(t), f) for t, f in zip(non_zero_tickers, freqs)])

    for i, freq in enumerate(feature['vector']):
        if i in ticker_idx:
            assert freq == freqs[ticker_idx.index(i)]
        else:
            assert freq == 0
