from sysadmin.views import *


@login_required
@active_page("download")
def index(request):
    return render(request, "sysadmin/download/index.html", {})
