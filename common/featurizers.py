import functools
from typing import Dict, Tuple, Callable, get_type_hints

from praw.reddit import Comment, Submission

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

Featurizer = Callable[[Comment, Comment, Submission, int], Dict]


def featurizer(version: int):
    def wrapped(func):
        @functools.wraps(func)
        def returned(comment: Comment, *args, **kwargs):
            result = func(comment, *args, **kwargs)

            return {'id': comment.id, 'name': func.__name__, 'version': version, 'features': result}

        return returned

    return wrapped


@featurizer(version=1)
def text_analysis(comment: Comment, root: Comment, thread: Submission, depth: int):
    d = {
        'body_to_parent': len(comment.body) / len(comment.parent().body) if depth != 0 else None,
        'body_to_root': len(comment.body) / len(root.body) if depth != 0 else None,
    }
    return d


@featurizer(version=1)
def info(comment: Comment, root: Comment, thread: Submission, depth: int):
    return {
        'depth': depth,
        'score': comment.score,
        'created_utc': comment.created_utc,
        'submission_id': comment.submission.id
    }


@featurizer(version=1)
def counter(comment: Comment, root: Comment, thread: Submission, depth: int):
    vector = [0] * len(tickers)
    for idx, t in enumerate(tickers):
        vector[idx] = comment.body.lower().count(t)
    return {'vector': vector}
