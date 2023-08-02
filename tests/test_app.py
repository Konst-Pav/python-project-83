import pytest
import requests


def test_home(client):
    response = client.get("/")
    assert b"<title>Page analyzer</title>" in response.data


def test_post_urls(client, app):
    response = client.post("/urls", data={'url': 'https://abracadabra.org/en-US/'})
    assert response.status_code == 200
