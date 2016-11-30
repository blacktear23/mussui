import logging
from optparse import OptionParser
from datetime import datetime, timedelta
from db.models import *


def do_expire_check():
    query = SSUser.objects.exclude(expire_date=None)
    for ssuser in query:
        if ssuser.is_expire():
            ssuser.disable()
            logging.info("User %s is expire" % ssuser.name)


def main(args):
    usage = 'usage: service.py %prog [options]'
    version = "%prog 1.0"
    opts = OptionParser(usage=usage, version=version)
    (options, args) = opts.parse_args(args)
    do_expire_check()
