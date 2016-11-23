from sysadmin.views import *


@login_required
def index(request):
    keyword = ""
    if "search" in request.GET:
        keyword = request.GET['search'].strip()
        filters = Q(hostname__icontains=keyword) | Q(ip__contains=keyword)
        query = Server.objects.filter(filters)
    else:
        query = Server.objects.all()

    data = {
        "servers": paginate(request, query),
        "search": keyword,
    }
    return render(request, "sysadmin/servers/index.html", data)


@login_required
@require_POST
def create(request):
    form = ServerForm(request.POST)
    if form.is_valid():
        server = Server()
        save_instance(form, server)
        return render_200("OK")
    return render_form_error(form)


@login_required
def detail(request, id):
    server = get_object_or_404(Server, pk=id)
    data = {
        "hostname": server.hostname,
        "ip": server.ip,
        "comments": server.comments,
    }
    return render_json(data)


@login_required
@require_POST
def edit(request, id):
    server = get_object_or_404(Server, pk=id)
    form = ServerForm(request.POST)
    if form.is_valid():
        save_instance(form, server)
        return render_200("OK")
    return render_form_error(form)


@login_required
def delete(request, id):
    server = get_object_or_404(Server, pk=id)
    server.delete()
    return redirect("/admin/servers")
