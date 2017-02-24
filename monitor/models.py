from django.db import models


class FlowStatistic(models.Model):
    userid = models.IntegerField(null=False)
    server_name = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(null=False)
    inbound_flow = models.IntegerField(null=False)
    outbound_flow = models.IntegerField(null=False)
    inbound_bandwidth = models.IntegerField(null=False)
    outbound_bandwidth = models.IntegerField(null=False)

    class Meta:
        app_label = 'monitor'
        db_table = "flow_statistic"
        unique_together = (('userid', 'date', 'server_name'), )


class ConnectionStatistic(models.Model):
    userid = models.IntegerField(null=False)
    server_name = models.CharField(max_length=255, null=False)
    date = models.DateTimeField(null=False)
    connections = models.IntegerField(null=False)

    class Meta:
        app_label = 'monitor'
        db_table = "connection_statistic"
        unique_together = (('userid', 'date', 'server_name'), )


class OperationLog(models.Model):
    operator = models.CharField(max_length=255, null=False, db_index=True)
    target = models.CharField(max_length=255, null=False, db_index=True)
    message = models.TextField(null=False, default="")
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'monitor'
        db_table = "operation_log"

    @classmethod
    def log(cls, operator, target, message):
        olog = OperationLog(operator=operator, target=target, message=message)
        olog.save()
        return olog
