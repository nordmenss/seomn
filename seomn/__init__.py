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

def execute_nocommit(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)

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
    result=loadrow("default","SELECT _connection_info.get('"+fqdn+"')")
    if result!=[]:
        params=result[0]
        ip=params[0]
        dbname=params[1]
        user=params[2]
        password=params[3]
        port=params[4]
        domain_id=params[5]
        schema='id_'+str(domain_id)
        settings.DATABASES['cluster']={'ENGINE':'postgresql_psycopg2','NAME':dbname,'USER':user, 'PASSWORD':password,'HOST':ip,'PORT':port,'DATABASE_SCHEMA':schema}
        execute('cluster','SET search_path to '+schema)
        return True
    else:
        return False
