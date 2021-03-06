from sysadmin.views import *


@login_required
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

    data = {
        "users": paginate(request, query),
        "search": keyword,
    }
    return render(request, "sysadmin/users/index.html", data)


@login_required
@require_POST
def create(request):
    if 'name' not in request.POST:
        return render_400("require name parameter")
    if 'servers' not in request.POST:
        return render_400("require servers parameter")
    try:
        servers = int(request.POST['servers'])
        if servers < 1:
            return render_400("servers should not less than 1")
    except:
        return render_400("servers parameter should be number")
    if 'bandwidth' not in request.POST:
        return render_400("require bandwidth parameter")
    try:
        bandwidth = int(request.POST['bandwidth'])
        if bandwidth < 1:
            return render_400("Bandwidth should not less than 1")
    except:
        return render_400("bandwidth parameter should be number")
    if 'password' not in request.POST:
        return render_400("require password parameter")
    password = request.POST['password']
    if len(password) < 6:
        return render_400("password should not less than 6 characters")
    name = request.POST['name']
    if name == "":
        return render_400("Name should not empty")
    dexpire = None
    if 'expire' in request.POST:
        expire = request.POST['expire']
        if expire != "":
            dexpire = parse_datetime(expire)
            if dexpire is None:
                return render_400("expire date is not valid")
            if dexpire < datetime.now():
                return render_400("expire date is before today")
    try:
        ssuser = SSUser.create(name, servers, bandwidth, password, dexpire)
    except Exception as e:
        return render_400("%s" % e)
    return render_200("OK")


@login_required
@require_POST
def edit(request, id):
    print request.POST
    ssuser = get_object_or_404(SSUser, pk=id)
    if 'bandwidth' not in request.POST:
        return render_400("require bandwidth parameter")
    try:
        bandwidth = int(request.POST['bandwidth'])
        if bandwidth < 1:
            return render_400("Bandwidth should not less than 1")
    except:
        return render_400("bandwidth parameter should be number")
    if 'servers' not in request.POST:
        return render_400("require servers parameter")
    try:
        servers = int(request.POST['servers'])
        if servers < 1:
            return render_400("servers should not less than 1")
    except:
        return render_400("servers parameter should be number")
    if 'bandwidth' not in request.POST:
        return render_400("require bandwidth parameter")
    password = request.POST.get('password', '')
    if password != "":
        if len(password) < 6:
            return render_400("password should not less than 6 character")
        ssuser.set_password(password, False)
    if 'expire' in request.POST:
        expire = request.POST['expire']
        if expire != "":
            dexpire = parse_datetime(expire)
            if dexpire is None:
                return render_400("expire date is not valid")
            ssuser.expire_date = dexpire
        else:
            ssuser.expire_date = None
    ssuser.bandwidth = bandwidth
    if servers != ssuser.number_server:
        ssuser.number_server = servers
        ssuser.auto_assign_servers(False)
    ssuser.save()
    return render_200("OK")


def render_ssuser(user):
    servers = user.get_servers()
    ret = {
        'name': user.name,
        'status': user.status,
        'password': user.password,
        'servers': servers,
        'expire': user.get_expire_str(),
        'is_expire': user.is_expire(),
    }
    return ret


@login_required
def details(request, id):
    user = get_object_or_404(SSUser, pk=id)
    return render_json(render_ssuser(user))


@login_required
def config(request, id):
    user = get_object_or_404(SSUser, pk=id)
    data = {
        "config": user.generate_config(),
    }
    return render_json(data)


@login_required
def enable(request, id):
    user = get_object_or_404(SSUser, pk=id)
    user.enable()
    return redirect("/admin/customers")


@login_required
def disable(request, id):
    user = get_object_or_404(SSUser, pk=id)
    user.disable()
    return redirect("/admin/customers")


@login_required
def delete(request, id):
    user = get_object_or_404(SSUser, pk=id)
    user.delete()
    return redirect("/admin/customers")
