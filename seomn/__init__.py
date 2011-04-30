VERSION = '0.0'
from django.conf import settings
from urlparse import urlparse
import datetime
from django.db import connections, transaction

def get_host(href):
    parse_object = urlparse(href)
    return parse_object.netloc

def get_path(href):
    parse_object = urlparse(href)
    return parse_object.path

@transaction.commit_manually()
def execute(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    transaction.commit_unless_managed(using=db)

def execute_nocommit(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)

def load_row(db,sql):
    cursor = connections[db].cursor()
    cursor.execute(sql)
    return cursor.fetchone()

def load_bool(db,sql):
    row=load_row(db,sql)
    if row!=None:
        return bool(row[0])
    return None

def load_int(db,sql):
    row=load_row(db,sql)
    if row!=None:
        return int(row[0])
    return None

def load_str(db,sql):
    row=load_row(db,sql)
    if row!=None:
        return str(row[0])
    return None

def load_date(db,sql):
    row=load_row(db,sql)
    if row!=None:
        return row[0]
    return None

def load_rows(db,sql):
    from django.db import connections, transaction
    cursor = connections[db].cursor()
    cursor.execute(sql)
    return cursor.fetchall()

def fqdn_redirect(fqdn):
    return settings.FORCE_SCRIPT_NAME+fqdn

def connect2db(fqdn):#make connection
    sql="select c.ip,c.dbname,c.username,c.pass,c.port,c.domain_id  FROM _connection_info.get('"+fqdn+"') as c"
    params=load_row("default",sql)
    if params!=[]:
        ip=params[0]
        dbname=params[1]
        user=params[2]
        password=params[3]
        port=params[4]
        domain_id=params[5]
        schema='id_'+str(domain_id)
        settings.DATABASES['cluster']={'ENGINE':'postgresql_psycopg2','NAME':dbname,'USER':user, 'PASSWORD':password,'HOST':ip,'PORT':port}
        execute_nocommit('cluster',"SELECT _domain.set("+str(domain_id)+");")
        return True
    else:
        return False
