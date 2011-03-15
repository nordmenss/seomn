VERSION = '0.0'
from django.conf import settings
from urlparse import urlparse
from django.db import connections

def get_host(href):
    parse_object = urlparse(href)
    return parse_object.netloc

def execute(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed(using=db)

def loadrow(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    return cursor.fetchone()

def loadrows(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def fqdn_redirect(fqdn):
    return settings.FORCE_SCRIPT_NAME+fqdn

def connect2db(fqdn):#make connection
    params=loadrow("main_db","SELECT _connection_info.get('"+fqdn+"')")
    ip=params.ip
    dbname=params.dbname
    user=params.username
    password=params.password
    port=params.port
    settings.DATABASES['cluster']={'ENGINE':'postgresql_psycopg2','NAME':dbname,'USER':user, 'PASSWORD':password,'HOST':ip,'PORT':port}