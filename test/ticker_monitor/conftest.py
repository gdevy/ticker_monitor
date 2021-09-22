import pytest


@pytest.fixture(scope='session', autouse=True)
def setup_env():
    import dotenv
    dotenv.load_dotenv('')
