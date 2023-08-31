from validators.url import url as validate


def validate_url(url):
    url_is_valid = validate(url) and len(url) <= 255
    return url_is_valid
