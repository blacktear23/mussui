import logging
from optparse import OptionParser
from datetime import datetime, timedelta
from monitor.models import *


def do_rotate_monitor_data(days=30):
    now = datetime.now()
    date = now - timedelta(days)
    for table in [FlowStatistic, ConnectionStatistic]:
        do_rotate_table(table, date)


def do_rotate_table(table, date):
    table_name = table()._meta.db_table
    logging.info("Rotate Table: %s" % table_name)
    query = table.objects.filter(date__lte=date)
    count = 0
    for item in query:
        item.delete()
        count += 1
    logging.info("Table %s rotate %d rows" % (table_name, count))


def main(args):
    usage = 'usage: service.py %prog [options]'
    version = "%prog 1.0"
    opts = OptionParser(usage=usage, version=version)
    (options, args) = opts.parse_args(args)
    do_rotate_monitor_data()
