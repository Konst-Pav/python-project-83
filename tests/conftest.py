import pytest
from page_analyzer.app import app as page_analyzer_app


@pytest.fixture()
def app():
    return page_analyzer_app


@pytest.fixture()
def client(app):
    return app.test_client()
