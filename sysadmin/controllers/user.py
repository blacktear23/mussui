from sysadmin.views import *


@login_required
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
    name = request.POST['name']
    if name == "":
        return render_400("Name should not empty")
    try:
        SSUser.create(name)
    except Exception as e:
        return render_400("%s" % e)
    return render_200("OK")


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
