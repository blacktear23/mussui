from sysadmin.views import *


@login_required
@load_license
@active_page("download")
def index(request):
    return render(request, "sysadmin/download/index.html", {})
