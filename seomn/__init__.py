VERSION = '0.0'

from urlparse import urlparse


def get_host(href):
    parse_object = urlparse(href)
    return parse_object.netloc