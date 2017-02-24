from sysadmin.views import *


@login_required
@load_license
@active_page("license")
def index(request):
    license = License.get()
    if license is None:
        license = License.initial()
    data = {
        "license": license,
        "config": license.get_config(),
    }
    return render(request, "sysadmin/license/index.html", data)


@login_required
@load_license
@require_POST
def update(request):
    if "license" not in request.POST:
        return render_400("Require license parameter")
    license = License.get()
    license.license = request.POST['license']
    license.save()
    log_request(request, "license", "Update license")
    return render_200("OK")
