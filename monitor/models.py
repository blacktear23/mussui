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
