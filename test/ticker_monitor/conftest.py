from pathlib import Path

import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_env():
    import dotenv
    p = Path(r"../.env.test")
    dotenv.load_dotenv(p)


@pytest.fixture(scope='session')
def praw_conn(setup_env):
    from ticker_monitor.common.praw_interface import auth_praw

    return auth_praw()
