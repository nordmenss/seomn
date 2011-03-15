VERSION = '0.0'

from urlparse import urlparse

def get_host(href):
    parse_object = urlparse(href)
    return parse_object.netloc

def execute(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed(using=db)