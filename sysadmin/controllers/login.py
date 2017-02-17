from django.db import connections
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.translation import ugettext as _

from sysadmin.views import *


# Return format:
# [
#   [{USER Object}, {inbound flow}, {outbound flow}]
#   ...
# ]
def calculate_top_flow_usage(start_date, limit):
    date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    sql = "SELECT userid, SUM(inbound_flow) AS `inbound`, SUM(outbound_flow) AS `outbound` FROM flow_statistic WHERE date > '%s' GROUP BY userid ORDER BY outbound DESC LIMIT %d" % (date_str, limit)
    row_ret = []
    user_ids = []
    with connections['monitor'].cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            row_ret.append(row)
            user_ids.append(row[0])

    udict = {}
    for user in SSUser.objects.filter(userid__in=user_ids):
        udict[user.userid] = user

    ret = []
    for item in row_ret:
        if item[0] not in udict:
            continue
        ret.append([udict[item[0]], item[1], item[2]])
    return ret


# Return format:
# [
#   [{USER Object}, {inbound bandwidth}, {outbound bandwidth}]
#   ...
# ]
def calculate_top_bandwidth_usage(start_date, limit):
    date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    sql = "SELECT userid, MAX(inbound_bandwidth) AS `inbound`, MAX(outbound_bandwidth) AS `outbound` FROM flow_statistic WHERE date > '%s' GROUP BY userid ORDER BY outbound DESC LIMIT %d " % (date_str, limit)
    row_ret = []
    user_ids = []
    with connections['monitor'].cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            row_ret.append(row)
            user_ids.append(row[0])

    udict = {}
    for user in SSUser.objects.filter(userid__in=user_ids):
        udict[user.userid] = user

    ret = []
    for item in row_ret:
        if item[0] not in udict:
            continue
        ret.append([udict[item[0]], item[1], item[2]])
    return ret


@login_required
@load_license
def total_bandwidth(request):
    start_date = datetime.now() - timedelta(days=1)
    date_str = start_date.strftime("%Y-%m-%d %H:%M:%S")
    sql = "SELECT date, SUM(inbound_bandwidth) AS `inbound`, SUM(outbound_bandwidth) AS `outbound` FROM flow_statistic WHERE date > '%s' GROUP BY date" % date_str
    ret = [[], []]
    with connections['monitor'].cursor() as cursor:
        cursor.execute(sql)
        for row in cursor.fetchall():
            dstr = row[0].strftime("%Y-%m-%d %H:%M")
            ret[0].append([dstr, int(row[1])])
            ret[1].append([dstr, int(row[2])])
    return render_json(ret)


@login_required
@load_license
@active_page('dashboard')
def index(request):
    start_date = datetime.now() - timedelta(days=1)
    data = {
        "number_customers": SSUser.objects.count(),
        "number_servers": Server.objects.count(),
        "top_10_flow_user": calculate_top_flow_usage(start_date, 10),
        "top_10_bandwidth_user": calculate_top_bandwidth_usage(start_date, 10),
    }
    return render(request, 'sysadmin/login/index.html', data)


def login_index(request):
    if request.user.is_authenticated():
        return redirect("/admin")
    return render(request, 'sysadmin/login/login.html', {})


def do_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect("/admin")
    return render(request, 'sysadmin/login/login.html', {'error_message': _('Login Error')})


@login_required
def do_logout(request):
    logout(request)
    return redirect("/admin/login")


@login_required
@require_POST
def change_password(request):
    password = request.POST['password']
    confirm = request.POST['confirm']
    if password != confirm:
        return render_json({'confirm': _("Confirm is not equals to password")}, 400)
    user = request.user
    user.set_password(password)
    user.save()
    update_session_auth_hash(request, user)
    return render_200("OK")
