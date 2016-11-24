from sysadmin.views import *


@login_required
def index(request):
    return render(request, "sysadmin/download/index.html", {})
