from sysadmin.views import *
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.utils.translation import ugettext as _


@login_required
@load_license
@active_page('dashboard')
def index(request):
    data = {
        "number_customers": SSUser.objects.count(),
        "number_servers": Server.objects.count(),
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
