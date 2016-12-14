from api.views import *


@require_POST
@user_authorize
def config(request, user):
    cfgdata = user.generate_config()
    return render_200(cfgdata)
