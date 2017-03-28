from sysadmin.views import *
from django.utils.translation import ugettext as _


@login_required
@load_license
@active_page("customer")
def index(request):
    keyword = ""
    if "search" in request.GET:
        keyword = request.GET['search'].strip()
        filters = Q(name__icontains=keyword)
        try:
            uid = int(keyword)
            filters |= Q(userid=uid)
        except:
            pass
        query = SSUser.objects.filter(filters)
    else:
        query = SSUser.objects.all()

    num_user = 0
    max_bw = 1
    try:
        num_user = int(request.license_config.get('numuser', 0))
        max_bw = int(request.license_config.get("maxbw", 1))
    except:
        pass
    servers = Server.objects.filter(status__in=["Enabled", "Full"])
    data = {
        "users": paginate(request, query),
        "search": keyword,
        "servers": servers,
        "default_bw": min(4, max_bw),
        "exceed": (SSUser.objects.count() >= num_user),
    }
    return render(request, "sysadmin/users/index.html", data)


@login_required
@load_license
@require_POST
def create(request):
    if request.license_config is None:
        return render_400("license is expired")
    else:
        num_user = int(request.license_config.get('numuser', 0))
        if SSUser.objects.count() >= num_user:
            return render_400(_("exceed number users quota"))

    if 'name' not in request.POST:
        return render_400(_("require name parameter"))
    if 'servers' not in request.POST:
        return render_400(_("require servers parameter"))
    try:
        servers = int(request.POST['servers'])
        if servers < 1:
            return render_400(_("servers should not less than 1"))
    except:
        return render_400(_("servers parameter should be number"))
    if 'bandwidth' not in request.POST:
        return render_400(_("require bandwidth parameter"))
    try:
        bandwidth = int(request.POST['bandwidth'])
        if bandwidth < 0:
            return render_400(_("Bandwidth should not less than %d") % 0)
        max_bandwidth = int(request.license_config.get("maxbw", 1))
        if bandwidth > max_bandwidth:
            return render_400(_("Bandwidth exceed max bandwidth quota"))
        min_bandwidth = 1
        if request.license.enable_unlimited_bandwidth():
            min_bandwidth = 0
        if bandwidth < min_bandwidth:
            return render_400(_("Bandwidth should not less than %d") % min_bandwidth)
    except:
        return render_400(_("bandwidth parameter should be number"))
    if 'password' not in request.POST:
        return render_400(_("require password parameter"))
    password = request.POST['password']
    if len(password) < 6:
        return render_400(_("password should not less than 6 characters"))
    name = request.POST['name']
    if name == "":
        return render_400(_("Name should not empty"))
    dexpire = None
    if 'expire' in request.POST:
        expire = request.POST['expire']
        if expire != "":
            dexpire = parse_datetime(expire)
            if dexpire is None:
                return render_400(_("expire date is not valid"))
            if dexpire < datetime.now():
                return render_400(_("expire date is before today"))
    try:
        ssuser = SSUser.create(name, servers, bandwidth, password, dexpire)
    except Exception as e:
        return render_400("%s" % e)
    log_request(request, ssuser.name, "Create new user")
    return render_200("OK")


@login_required
@load_license
@require_POST
def edit(request, id):
    if request.license_config is None:
        return render_400(_("license is expired"))
    ssuser = get_object_or_404(SSUser, pk=id)
    message = "Update user"

    if 'bandwidth' not in request.POST:
        return render_400(_("require bandwidth parameter"))
    try:
        bandwidth = int(request.POST['bandwidth'])
        if bandwidth < 0:
            return render_400(_("Bandwidth should not less than %d") % 0)
        max_bandwidth = int(request.license_config.get("maxbw", 1))
        if bandwidth > max_bandwidth:
            return render_400(_("Bandwidth exceed max bandwidth quota"))
        min_bandwidth = 1
        if request.license.enable_unlimited_bandwidth():
            min_bandwidth = 0
        if bandwidth < min_bandwidth:
            return render_400(_("Bandwidth should not less than %d") % min_bandwidth)
    except:
        return render_400(_("bandwidth parameter should be number"))

    if 'servers' not in request.POST:
        return render_400(_("require servers parameter"))
    try:
        servers = int(request.POST['servers'])
        if servers < 1:
            return render_400(_("servers should not less than 1"))
    except:
        return render_400(_("servers parameter should be number"))

    password = request.POST.get('password', '')
    if password != "":
        if len(password) < 6:
            return render_400(_("password should not less than 6 character"))
        message += " change password"
        ssuser.set_password(password, False)

    if 'expire' in request.POST:
        expire = request.POST['expire']
        if expire != "":
            dexpire = parse_datetime(expire)
            if dexpire is None:
                return render_400(_("expire date is not valid"))
            if ssuser.expire_date != dexpire:
                message += " change expire date from %s to %s" % (ssuser.expire_date, dexpire)
            ssuser.expire_date = dexpire
        else:
            if ssuser.expire_date is not None:
                message += " change expire date from %s to %s" % (ssuser.expire_date, 'None')
            ssuser.expire_date = None

    if 'server_list' in request.POST:
        server_list = request.POST['server_list'].split(",")
        if len(server_list) > servers:
            return render_400(_("you can choose no more than %d servers") % servers)
        # For now we just assign the server to servers
        if len(server_list) == servers:
            qserver = Server.objects.filter(id__in=server_list)
            ssuser.replace_servers(qserver)
            if servers != ssuser.number_server:
                message += " change number server from %s to %s" % (ssuser.number_server, servers)
                ssuser.number_server = servers
        else:
            # assigned server is less than just call auto assign
            if servers != ssuser.number_server:
                ssuser.number_server = servers
                ssuser.auto_assign_servers()

    if ssuser.bandwidth != bandwidth:
        message += " change bandwidth from %s to %s" % (ssuser.bandwidth, bandwidth)
    ssuser.bandwidth = bandwidth
    ssuser.save()
    log_request(request, ssuser.name, message)
    return render_200("OK")


def render_ssuser(user):
    servers = user.get_servers()
    ret = {
        'name': user.name,
        'status': user.status,
        'password': user.password,
        'bandwidth': user.bandwidth,
        'servers': servers,
        'expire': user.get_expire_str(),
        'is_expire': user.is_expire(),
    }
    return ret


@login_required
@load_license
def details(request, id):
    user = get_object_or_404(SSUser, pk=id)
    return render_json(render_ssuser(user))


@login_required
@load_license
def config(request, id):
    user = get_object_or_404(SSUser, pk=id)
    data = {
        "config": user.generate_config(),
    }
    return render_json(data)


@login_required
@load_license
def enable(request, id):
    user = get_object_or_404(SSUser, pk=id)
    user.enable()
    log_request(request, user.name, "Enable user")
    return redirect("/admin/customers")


@login_required
@load_license
def disable(request, id):
    user = get_object_or_404(SSUser, pk=id)
    user.disable()
    log_request(request, user.name, "Disable user")
    return redirect("/admin/customers")


@login_required
@load_license
def delete(request, id):
    user = get_object_or_404(SSUser, pk=id)
    log_request(request, user.name, "Delete user")
    user.delete()
    return redirect("/admin/customers")
