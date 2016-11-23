import random
import hashlib
from datetime import datetime
from django.db import models


def generate_user_id(start=1000, end=99000):
    for i in range(10):
        uid = random.randrange(start, end)
        if SSUser.objects.filter(userid=uid).count() <= 0:
            return uid
    return None


class SSUser(models.Model):
    STATUS = ['Enabled', 'Disabled']
    name = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    userid = models.IntegerField(null=False, db_index=True)
    password = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=20, null=False, default="Enabled")
    bandwidth = models.IntegerField(null=False, default=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "user"

    @classmethod
    def create(cls, name):
        query = SSUser.objects.filter(name=name)
        if query.count() > 0:
            raise Exception("Name already exists")
        uid = generate_user_id()
        if uid is None:
            raise Exception("Cannot generate userid")
        user = SSUser(userid=uid, name=name, status=SSUser.STATUS[0])
        user.generate_password()
        user.save()

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


class FlowStatistic(models.Model):
    userid = models.IntegerField(null=False)
    server_name = models.CharField(max_length=255, null=False)
    inbound_flow = models.IntegerField(null=False)
    outbound_flow = models.IntegerField(null=False)
    inbound_bandwidth = models.IntegerField(null=False)
    outbound_bandwidth = models.IntegerField(null=False)
    date = models.DateTimeField(null=False)

    class Meta:
        unique_together = (('userid', 'date', 'server_name'), )


class Server(models.Model):
    hostname = models.CharField(max_length=255, null=False, db_index=True, unique=True)
    ip = models.GenericIPAddressField(null=False)
    comments = models.TextField(null=False, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
