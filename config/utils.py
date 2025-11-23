import os, hashlib
from uuid import uuid4
from django.db import models

def alumni_photo(instance, filename):
    upload_to = 'Alumni_data/{}'.format(instance.registration_no)
    field = 'Foto'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_{}.{}'.format(field, instance.registration_no, ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)

def upload_profile(instance, filename):
    upload_to = 'users_profiles/'
    field = 'Foto_profile'
    ext = filename.split('.')[-1]
    if instance.pk:
        filename = '{}_{}.{}'.format(field, instance.first_name,ext)
    else:
        filename = '{}.{}'.format(uuid4().hex, ext)
    return os.path.join(upload_to, filename)


def getlastid(table_name):
    result = table_name.objects.last()
    if result:
        lastid = result.id
        newid = lastid + 1
    else:
        lastid = 0
        newid = 1
    return lastid, newid
def getnewid(table_name):
    result = table_name.objects.last()
    if result:
        newid = result.id + 1
        hashid = hashlib.md5(str(newid).encode())
    else:
        newid = 1
        hashid = hashlib.md5(str(newid).encode())
    return newid, hashid.hexdigest()

def getjustnewid(table_name):
    result0 = table_name.objects.all()
    if result0.count() > 0:
        result = table_name.objects.last()
        if result:
            newid = result.id + 1
    else:
        newid = 1
    return newid

def hash_md52(strhash):
    hashed = hashlib.md5(strhash.encode())
    return hashed.hexdigest()

def hash_md5(value):
    value_str = str(value)
    hashed = hashlib.md5(value_str.encode())
    return hashed.hexdigest()

def split_string(string):
    string2 = string.split()
    return string2[0].lower()


class UUIDField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length='] = 32
        kwargs['unique'] = True
        kwargs['default'] = uuid.uuid4
        super().__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'char(32)'