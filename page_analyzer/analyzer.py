import requests
from requests import RequestException
from bs4 import BeautifulSoup


def url_check(url):
    try:
        response = requests.get(url)
    except RequestException:
        return None
    status_code = response.status_code
    parsed_response = BeautifulSoup(response.text, 'html.parser')
    h1 = parsed_response.h1.string if parsed_response.h1 else ''
    title = parsed_response.title.string if parsed_response.title else ''
    tag_with_description = parsed_response.find('meta', attrs={'name': 'description'}, content=True)
    description = tag_with_description['content'] if tag_with_description else ''
    result = {'url': url, 'status_code': status_code, 'h1': h1, 'title': title, 'description': description}
    return result
