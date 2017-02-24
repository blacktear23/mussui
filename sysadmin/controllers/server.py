from sysadmin.views import *


@login_required
@load_license
@active_page("server")
def index(request):
    keyword = ""
    if "search" in request.GET:
        keyword = request.GET['search'].strip()
        filters = Q(hostname__icontains=keyword) | Q(ip__contains=keyword)
        query = Server.objects.filter(filters)
    else:
        query = Server.objects.all()
    num_server = 0
    try:
        num_server = int(request.license_config.get('numserver', 0))
    except:
        pass
    data = {
        "servers": paginate(request, query),
        "search": keyword,
        "exceed": (Server.objects.count() >= num_server),
    }
    return render(request, "sysadmin/servers/index.html", data)


@login_required
@load_license
@require_POST
def create(request):
    if request.license_config is None:
        return render_json({"hostname": "license is expired"}, 400)
    else:
        num_server = int(request.license_config.get('numserver', 0))
        if Server.objects.count() >= num_server:
            return render_json({"hostname": "exceed number servers quota"}, 400)
    form = ServerForm(request.POST)
    if form.is_valid():
        server = Server()
        save_instance(form, server)
        log_request(request, server.hostname, "Create new server")
        return render_200("OK")
    return render_form_error(form)


@login_required
@load_license
def detail(request, id):
    server = get_object_or_404(Server, pk=id)
    data = {
        "hostname": server.hostname,
        "ip": server.ip,
        "port": server.port,
        "status": server.status,
        "encryption": server.encryption,
        "comments": server.comments,
    }
    return render_json(data)


@login_required
@load_license
@require_POST
def edit(request, id):
    if request.license_config is None:
        return render_json({"hostname": "license is expired"}, 400)
    server = get_object_or_404(Server, pk=id)
    message = "Update server"
    form = ServerForm(request.POST)
    if form.is_valid():
        cdata = form.cleaned_data
        if cdata['status'] != server.status:
            message += " change status from %s to %s" % (server.status, cdata['status'])
        if cdata['hostname'] != server.hostname:
            message += " change hostname from %s to %s" % (server.hostname, cdata['hostname'])
        if cdata['encryption'] != server.encryption:
            message += " change encryption from %s to %s" % (server.encryption, cdata['encryption'])
        save_instance(form, server)
        log_request(request, server.hostname, message)
        return render_200("OK")
    return render_form_error(form)


@login_required
@load_license
def delete(request, id):
    server = get_object_or_404(Server, pk=id)
    log_request(request, server.hostname, "Delete server")
    server.delete()
    return redirect("/admin/servers")
