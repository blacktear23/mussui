import rsa
import json
import redis
import base64
import random
import logging
import hashlib
from uuid import getnode
from datetime import datetime
from django.db import models
from mussui import config


def generate_user_id(start=1000, end=99000):
    for i in range(10):
        uid = random.randrange(start, end)
        if SSUser.objects.filter(userid=uid).count() <= 0:
            return uid
    return None


def load_public_key():
    pk = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEA11LzgDq5c2Ts3eSQ95wvt6Lqm5KT86X81ofTD23mZYoStX7qg4Qu
TeT3UOrjcMzGJ/zFSkU0d+A9My5zlp4fN+wozuOXQHo/bbMDG46s2fMkHxT/h+kY
sXUfJIURJ12N1FaSOhCSToIHCr9jbm7aQgECqPHTTQz1chl3BA2ggDPkD16gHxc1
Up2a6GbONE5o0h/OpFsT3qJueNR2gYfkACiBONj2yY6YINyMgKDrKvcY5/nmi5zg
HOKYis4QzQ4f3HmUyKfCrRkvWa0e+rZL6/nl0zcSk2338+zDV7zxkRa/iXxaDMee
LclgkDFsEMY/3Ytfeiiz0mV4nqKdUMsAfQIDAQAB
-----END RSA PUBLIC KEY-----"""
    return rsa.PublicKey.load_pkcs1(pk)


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
    servers = models.ManyToManyField("Server")

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
        user.set_password(password, False)
        user.save()
        user.auto_assign_servers()

    @classmethod
    def get_by_name(cls, username):
        query = SSUser.objects.filter(name=username, status="Enabled")
        if len(query) == 0:
            return None
        return query[0]

    @classmethod
    def authorization(cls, username, password):
        hpassword = hashlib.sha256(password).hexdigest()
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

    def server_ids(self):
        return ",".join([str(server.id) for server in self.servers.all()])

    def replace_servers(self, new_servers):
        self_servers = [s.id for s in self.servers.all()]
        need_replace = False
        for ns in new_servers:
            if ns.id not in self_servers:
                need_replace = True
                break
        if need_replace:
            self.servers.clear()
            for ns in new_servers:
                self.servers.add(ns)

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

    def auto_assign_servers(self):
        self.servers.clear()
        servers = list(Server.objects.filter(status="Enabled"))
        ret = set()
        loop_times = min(self.number_server, len(servers))
        random.shuffle(servers)
        for i in range(loop_times):
            server = servers[i]
            self.servers.add(server)

    def get_servers(self):
        if self.servers.count() == 0:
            self.auto_assign_servers()
        query = self.servers.filter(status__in=['Enabled', 'Full'])
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


class License(models.Model):
    fingerprint = models.CharField(max_length=255, null=False)
    license = models.TextField(null=True, blank=True, default="")

    @classmethod
    def initial(cls):
        query = License.objects.all()
        if len(query) != 0:
            l = query[0]
            if l.fingerprint != "":
                return
        license = License(fingerprint="")
        license.check_finger_print()
        license.save()
        return license

    @classmethod
    def get_or_init(cls):
        license = License.get()
        if license is None:
            license = License.initial()
        return license

    @classmethod
    def get(cls):
        query = License.objects.all()
        if len(query) > 0:
            license = query[0]
            license.check_finger_print()
            return license
        return None

    def check_finger_print(self):
        finger_print = hashlib.sha1(str(getnode())).hexdigest()
        if self.fingerprint == "":
            self.fingerprint = finger_print
        else:
            if self.fingerprint != finger_print:
                self.fingerprint = finger_print
                self.save()

    def __load_config(self, data):
        ret = {}
        pairs = data.split("|")
        for pair in pairs:
            kvpair = pair.split(":")
            if len(kvpair) != 2:
                continue
            key, value = kvpair
            ret[key] = value
        return ret

    def get_config(self):
        try:
            data = self.__load_config(base64.decodestring(self.license))
            pconf, sign = base64.decodestring(data['config']), base64.decodestring(data['sign'])
            pubkey = load_public_key()
            verify = rsa.verify(pconf + self.fingerprint, sign, pubkey)
            if verify:
                return self.__load_config(pconf)
        except Exception, e:
            pass
        return None

    def expired(self):
        cfg = self.get_config()
        if cfg is None or 'expire' not in cfg:
            return True
        expire = datetime.strptime(cfg['expire'], "%Y-%m-%d")
        return expire <= datetime.now()
