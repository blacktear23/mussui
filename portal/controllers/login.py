from portal.views import *


def login_index(request):
    if is_logined(request):
        return redirect("/")
    return render(request, 'portal/login/login.html', {})


def do_login(request):
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
