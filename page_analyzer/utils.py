from urllib.parse import urlparse, urlunparse

import validators


def is_valid(url: str) -> bool:
    '''Validates url by cheking its length and format'''

    return len(url) < 255 and validators.url(url)
    

def normalize_url(url: str) -> str:
    '''Normalizes a URL by removing the path, query parameters, and fragments,
    leaving only the scheme and domain.'''
    
    parsed_url = urlparse(url)
    normalized_url = urlunparse((parsed_url.scheme, parsed_url.netloc, 
                                 '', '', '', ''))
    return normalized_url
