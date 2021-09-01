import logging
import os
from typing import Union, Callable, List, Dict

import dotenv

import praw
from praw.models import MoreComments
from praw.models.comment_forest import CommentForest
from praw.reddit import Comment, Submission

from common.featurizers import Featurizer

logger = logging.getLogger(__name__)


def auth_praw() -> praw.Reddit:
    dotenv.load_dotenv()

    reddit = praw.Reddit(
        client_id=os.environ['REDDIT_APP_ID'],
        client_secret=os.environ['REDDIT_APP_SECRET'],
        username=os.environ['REDDIT_USERNAME'],
        password=os.environ['REDDIT_PASSWORD'],
        user_agent=f"ticker_monitor/0.1 by {os.environ['REDDIT_USERNAME']}",
    )

    logger.debug(f'logged in as {reddit.user.me(use_cache=False)}')

    return reddit


def print_comment_chain(comment: Union[Comment, MoreComments], depth=0):
    if isinstance(comment, Comment):
        for line in comment.body.split('\n'):
            print(f"{' ' * depth}| {line}")
    elif isinstance(comment, MoreComments):
        print(f"{' ' * depth}| more comments")
        return

    for reply in comment.replies:
        print_comment_chain(reply, depth + 1)


def iterate_comment_forest(
        comment_forest: CommentForest,
        featurizers: List[Featurizer],
        depth=0,
        thread: Submission = None,
        root: Comment = None
) -> List[Dict]:
    results = []
    for comment in comment_forest:
        if isinstance(comment, MoreComments):
            continue
        if depth == 0:
            root = comment
        for f in featurizers:
            features = f(comment, root, thread, depth)
            print(features)
        next_results = iterate_comment_forest(comment.replies, featurizers, depth + 1, thread, root)
        results.extend(next_results)

    return results