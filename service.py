#!/usr/bin/env python
import os
import sys
import glob

# Setup Environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mussui.settings")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def help():
    print """services.py [service name] arg1 arg2 arg3 ..."""
    list_services()


def run_service():
    if len(sys.argv) <= 1:
        help()
        exit(0)
    import django
    django.setup()
    module_name = "services.%s_service" % sys.argv[1]
    module = __import__(module_name, globals(), locals(), ['main'])
    module.main(sys.argv[1:])


def list_services():
    services_dir = BASE_DIR + "/services/*_service.py"
    file_list = glob.glob(services_dir)
    print "services: "
    for fname in file_list:
        if fname.find("__init__") >= 0:
            continue
        service_name = fname.split("/")[-1][:-11]
        print "   %s" % (service_name)


if __name__ == "__main__":
    run_service()
