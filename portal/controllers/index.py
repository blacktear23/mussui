from portal.views import *


@ulogin_required
def index(request):
    ssuser = request.ssuser
    data = {
        'user': ssuser,
        'config': ssuser.generate_config(),
    }
    return render(request, 'portal/index/index.html', data)
