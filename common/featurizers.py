import functools
import logging
from typing import Dict, Callable, List

from praw.reddit import Comment, Submission

logger = logging.getLogger(__name__)

tickers = ['AMC', 'CLOV', 'BABA', 'GME', 'SPY', 'WISH', 'PLTR', 'FAS', 'SKLZ', 'PFE', 'MVST', 'CRSR', 'MSFT', 'BB',
           'HOOD', 'GEO', 'CLNE', 'TSLA', 'MRNA', 'SOFI', 'AVPT', 'CLF', 'AMZN', 'YOU', 'DDD', 'NVDA', 'BIDU', 'TLRY',
           'HD', 'SPRT', 'BARK', 'NIO', 'AMAT', 'AMD', 'Z', 'GM', 'COIN', 'EXPI', 'NFLX', 'NAKD', 'NOW', 'BOX', 'ARKK',
           'REED', 'NET', 'PSFE', 'SNDL', 'PTRA', 'AMRN', 'EDR', 'ZIM', 'MSTR', 'PINS', 'WEN', 'MAXR', 'HCMC', 'STEM',
           'WISA', 'AAL', 'ASTR', 'TIGR', 'VSTO', 'SWBI', 'CME', 'NNDM', 'TGT', 'HUT', 'VIAC', 'LUMN', 'RKT', 'MKD',
           'PAYA', 'CRTX', 'QFIN', 'GAIN', 'UAL', 'CGC', 'HYLN', 'BLND', 'RBLX', 'IDAI', 'SESN', 'WMT', 'OPTT', 'RSI',
           'SHOP', 'CHWY', 'RUN', 'GOTU', 'UPST', 'SDC', 'LABD', 'WKHS', 'FSR', 'WOOF', 'ASO', 'MVIS', 'FINV', 'HIMS',
           'MAPS', 'MT', 'NUE', 'EXAS', 'QD', 'OTLY', 'LVS', 'ARVL', 'PENN', 'EGLX', 'XELA', 'MCD', 'CANO', 'TEAM',
           'SPCE', 'LMND', 'ATER', 'MCFE', 'OCGN', 'THS', 'GOCO', 'LAZR', 'SE', 'DDS', 'UWMC', 'CHRS', 'KEN', 'DOCN',
           'AAPL', 'PRTY', 'CHPT', 'INVZ', 'ZY', 'SGOC', 'TAN', 'ED', 'KAR', 'FRI', 'EPI', 'SQQQ', 'ZNGA', 'VZIO',
           'MSGS', 'BITF', 'ROOT', 'SKIN', 'AYTU', 'CLSK']

tickers = list(map(str.lower, tickers))

Featurizer = Callable[[Comment, Submission, int], Dict]


def extract_features(
        comment: Comment,
        thread: Submission,
        depth: int,
        featurizers: List[Featurizer],
) -> List[Dict]:
    features = []

    for f in featurizers:
        feature = f(comment, thread, depth)
        logger.debug(feature)
        features.append(feature)

    return features


def comment_info(comment: Comment, depth: int):
    return {
        'depth': depth,
        'score': comment.score,
        'created_utc': comment.created_utc,
        'submission_id': comment.submission.id
    }


def featurizer(version: int):
    def wrapped(func):
        @functools.wraps(func)
        def returned(comment: Comment, *args, **kwargs):
            result = func(comment, *args, **kwargs)

            return {
                'name': func.__name__,
                'version': version,
                'comment_id': comment.id,
                **result}

        return returned

    return wrapped


@featurizer(version=1)
def text_analysis(comment: Comment, thread: Submission, depth: int):
    d = {
        'body_to_parent': len(comment.body) / len(comment.parent().body) if depth != 0 else None,
        'body_to_submission': len(comment.body) / len(thread.selftext) if depth != 0 else None,
    }
    return d


@featurizer(version=1)
def counter(comment: Comment, thread: Submission, depth: int):
    vector = [0] * len(tickers)
    for idx, t in enumerate(tickers):
        vector[idx] = comment.body.lower().count(t)
    return {'vector': vector}
