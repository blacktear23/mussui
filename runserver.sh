#! /bin/sh
BASE_DIR=`dirname $0`
WORK_DIR=`pwd`/$BASE_DIR
LOG_DIR=$BASE_DIR/log
UWSGI_PID_FILE=`pwd`/$LOG_DIR/uwsgi.pid
SCRIPT_NAME=runserver.sh
PYTHON_PATH=`which python`
INI_FILE=$WORK_DIR/uwsgi.ini

start_web() {
    echo Start uWSGI Server
    uwsgi --ini $INI_FILE
}

stop_web() {
    if [ -f $UWSGI_PID_FILE ]; then
        echo Stop uWSGI Server
        uwsgi --stop $UWSGI_PID_FILE
        rm -f $UWSGI_PID_FILE
    fi
}

reload_web() {
    if [ -f $UWSGI_PID_FILE ]; then
        echo Reload uWSGI Server
        uwsgi --reload $UWSGI_PID_FILE
    else
        start_web
    fi
}

migrate() {
    $PYTHON_PATH ./manage.py migrate
    $PYTHON_PATH ./manage.py migrate --database=monitor
}

install_cron() {
    if crontab -l | grep "service.py $1"; then
        echo "Already have cron job for $1"
    else
        echo "Install cron job for $1"
        TMP_FILE=crontab-temp.tmp
        crontab -l > $TMP_FILE
        echo "$2 $PYTHON_PATH $WORK_DIR/service.py $1 > /dev/null 2>&1" >> $TMP_FILE
        crontab $TMP_FILE
        rm $TMP_FILE
    fi
}

install_rotate() {
    # Every day 3:00 AM
    install_cron "rotate" "0 3 * * *"
}

case $1 in
    start-web):
        start_web
        ;;
    stop-web)
        stop_web
        ;;
    restart-web)
        reload_web
        ;;
    migrate)
        migrate
        ;;
    install-rotate)
        install_rotate
        ;;
    *)
        echo "Usage: $SCRIPT_NAME (start-web|stop-web|restart-web|migrate)"
        ;;
esac
