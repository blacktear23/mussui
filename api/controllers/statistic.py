from datetime import *
from django.db import connection
from api.views import *


@require_POST
@csrf_exempt
def post_data(request):
    data = json.loads(request.body, encoding="utf-8")
    process_data(data)
    return render_json({"status": "OK"})


def validate_host(hostname):
    count = Server.objects.filter(hostname=hostname).count()
    return count > 0


def process_data(data):
    # in different date
    for item in data:
        process_host_data(item)


# data is a list contains many instance
def process_host_data(data):
    for instance in data:
        process_instance_data(instance)


def process_instance_data(instance):
    date = datetime.strptime(instance['date'], "%Y-%m-%d %H:%M")
    host = instance['host']
    if not validate_host(host):
        return
    userid = int(instance['instance'])
    bw_data = instance['bandwidth']
    flow_in = int(bw_data['inbound'])
    flow_out = int(bw_data['outbound'])
    bw_in = flow_in * 8 / 300
    bw_out = flow_out * 8 / 300
    fs = FlowStatistic(userid=userid,
                       server_name=host,
                       date=date)
    fs.inbound_flow = flow_in
    fs.outbound_flow = flow_out
    fs.inbound_bandwidth = bw_in
    fs.outbound_bandwidth = bw_out
    fs.save()


def generate_sql(userid, tstart, tend):
    tstart_str = tstart.strftime("%Y-%m-%d %H:%M:%S")
    tend_str = tend.strftime("%Y-%m-%d %H:%M:%S")
    sql = "SELECT userid, date, SUM(inbound_bandwidth), SUM(outbound_bandwidth) FROM db_flowstatistic WHERE userid='%s' AND date BETWEEN '%s' AND '%s' GROUP BY date" % (userid, tstart_str, tend_str)
    return sql


def user_bandwidth(request):
    if 'userid' not in request.GET:
        return render_json_error("Require userid parameter")
    userid = request.GET['userid']
    now = datetime.now()
    one_day_before = now - timedelta(days=1)
    sql = generate_sql(userid, one_day_before, now)
    ret = [[], []]
    with connection.cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            date_str = row[1].strftime("%Y-%m-%d %H:%M")
            ret[0].append([date_str, int(row[2])])
            ret[1].append([date_str, int(row[3])])
    return render_json(ret)
