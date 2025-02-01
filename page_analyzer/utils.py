from urllib.parse import urlparse, urlunparse

import validators


def is_valid(url):
    if len(url) < 255 and validators.url(url):
        return True
    

def normalize_url(url):
    parsed_url = urlparse(url)
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, 
                                 '', '', '', ''))
    return normalized_url
