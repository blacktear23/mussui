import json
import redis
import random
import logging
import hashlib
from datetime import datetime
from django.db import models
from mussui import config


def generate_user_id(start=1000, end=99000):
    for i in range(10):
        uid = random.randrange(start, end)
        if SSUser.objects.filter(userid=uid).count() <= 0:
            return uid
    return None


__REDIS_CONN_POOL__ = None


def get_redis_connection():
    global __REDIS_CONN_POOL__
    if not config.REDIS['use']:
        return None
    if __REDIS_CONN_POOL__ is None:
        pool = redis.ConnectionPool(
            max_connections=100,
            host=config.REDIS['host'],
            port=config.REDIS['port'],
            db=config.REDIS['db']
        )
        __REDIS_CONN_POOL__ = pool
    return redis.Redis(connection_pool=__REDIS_CONN_POOL__)


def clean_cache(userid):
    try:
        conn = get_redis_connection()
        if conn is None:
            return
        conn.delete(str(userid))
    except Exception as e:
        logging.exception(e)


class SSUser(models.Model):
    STATUS = ['Enabled', 'Disabled']
    name = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    userid = models.IntegerField(null=False, db_index=True)
    password = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=20, null=False, default="Enabled")
    bandwidth = models.IntegerField(null=False, default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    servers_cache = models.CharField(max_length=1024, null=False, default="")
    number_server = models.IntegerField(null=False, default=1)
    login_password = models.CharField(max_length=255, null=False, default="")
    expire_date = models.DateTimeField(null=True)

    class Meta:
        db_table = "user"

    @classmethod
    def create(cls, name, servers, bandwidth, password, expire=None):
        query = SSUser.objects.filter(name=name)
        if query.count() > 0:
            raise Exception("Name already exists")
        uid = generate_user_id()
        if uid is None:
            raise Exception("Cannot generate userid")
        user = SSUser(userid=uid, name=name, status=SSUser.STATUS[0], number_server=servers, bandwidth=bandwidth, expire_date=expire)
        user.generate_password()
        user.auto_assign_servers(False)
        user.set_password(password, False)
        user.save()

    @classmethod
    def authorization(cls, username, password):
        hpassword = hashlib.sha256(password).hexdigest()
        print username, hpassword
        users = SSUser.objects.filter(name=username, status="Enabled", login_password=hpassword)
        if len(users) == 0:
            return None
        return users[0]

    def get_expire_str(self):
        if self.expire_date is None:
            return ""
        return self.expire_date.strftime("%Y-%m-%d")

    def is_expire(self):
        if self.expire_date is None:
            return False
        now = datetime.now()
        return now > self.expire_date

    def set_password(self, password, save=True):
        h = hashlib.sha256(password)
        self.login_password = h.hexdigest()
        if save:
            self.save()

    # Override save method
    def save(self):
        super(SSUser, self).save()
        clean_cache(self.userid)

    def generate_password(self):
        seed = "%s-%s" % (str(datetime.now()), self.userid)
        h = hashlib.md5(seed)
        self.password = h.hexdigest()

    def enable(self):
        self.status = SSUser.STATUS[0]
        self.save()

    def disable(self):
        self.status = SSUser.STATUS[1]
        self.save()

    def auto_assign_servers(self, save=True):
        servers = list(Server.objects.filter(status="Enabled"))
        ret = set()
        loop_times = min(self.number_server, len(servers))
        random.shuffle(servers)
        for i in range(loop_times):
            server = servers[i]
            ret.add(server.id)
        self.servers_cache = json.dumps(list(ret))
        if save:
            self.save()

    def get_servers(self):
        if self.servers_cache == "":
            self.auto_assign_servers()
        servers = json.loads(self.servers_cache)
        query = Server.objects.filter(id__in=servers, status__in=["Enabled", "Full"])
        ret = []
        for server in query:
            ret.append([server.hostname, "%s:%s" % (server.ip, server.port), "%s-auth" % server.encryption])
        return ret

    def generate_config(self):
        server_password = []
        for server in self.get_servers():
            item = [server[1], self.password, server[2]]
            server_password.append(item)
        cfg_data = {
            "local_port": 7070,
            "auth": True,
            "user_id": self.userid,
            "server_password": server_password,
        }
        return json.dumps(cfg_data, indent=4, sort_keys=True)


class Server(models.Model):
    ENCRYPTION_METHODS = [
        'aes-128-cfb',
        'aes-192-cfb',
        'aes-256-cfb',
        'rc4-md5',
    ]
    STATUS = [
        'Enabled',
        'Disabled',
        'Full',
    ]
    hostname = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    ip = models.GenericIPAddressField(null=False)
    port = models.IntegerField(null=False, default=8387)
    status = models.CharField(max_length=20, null=False, default="Enabled")
    encryption = models.CharField(max_length=50, null=False, default="aes-128-cfb")
    comments = models.TextField(null=False, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
