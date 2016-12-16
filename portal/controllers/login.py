from portal.views import *


def login_index(request):
    if is_logined(request):
        return redirect("/")
    return render(request, 'portal/login/login.html', {})


def do_login(request):
    if 'username' not in request.POST:
        return render(request, 'portal/login/login.html', {'error_message': 'Login Error'})
    if 'password' not in request.POST:
        return render(request, 'portal/login/login.html', {'error_message': 'Login Error'})
    username = request.POST['username']
    password = request.POST['password']
    user = SSUser.authorization(username, password)
    if user is not None:
        request.session['user_id'] = user.id
        return redirect("/")
    return render(request, 'portal/login/login.html', {'error_message': 'Login Error'})


@ulogin_required
def do_logout(request):
    del request.session['user_id']
    return redirect("/login")


@ulogin_required
@require_POST
def change_password(request):
    password = request.POST['password']
    confirm = request.POST['confirm']
    if len(password) < 6:
        return render_json({'password': "Password is too short"}, 400)
    if password != confirm:
        return render_json({'confirm': "Confirm is not equals to password"}, 400)
    ssuser = request.ssuser
    ssuser.set_password(password)
    return render_200("OK")
