import json
import hmac
import hashlib
from functools import wraps
from datetime import datetime
from django.shortcuts import *
from django.db.models import Q
from django.http import *
from django.template.base import add_to_builtins
from django.forms.models import model_to_dict, save_instance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import *
from django.views.decorators.csrf import csrf_exempt
from db.models import *
from monitor.models import *


def render_200(msg="<h1>HTTP 200 OK</h1>"):
    return HttpResponse(msg, status=200)


def render_400(msg=""):
    return HttpResponse(msg, status=400, content_type="text/plan")


def render_403(msg=""):
    return HttpResponse(msg, status=403, content_type="text/plan")


def render_404(msg=""):
    return HttpResponse(msg, status=404, content_type="text/plan")


def render_404_page(request):
    return render(request, "404.haml", {})


def render_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="text/json", status=status)


def render_json_error(errormsg, status=400):
    return render_json({'error': errormsg}, status)


def validate_sign(request, user):
    username = request.POST['username']
    req_sign = request.POST['sign'].lower()
    sign = hmac.new(str(user.login_password), request.method.upper() + "\n", hashlib.sha1)
    sign.update(str(request.path) + "\n")
    sign.update(str(username) + "\n")
    hsign = sign.hexdigest()
    print req_sign, hsign
    return req_sign == hsign


def user_authorize(func):
    @wraps(func)
    def _wrapper(request, *args, **kwargs):
        if 'username' not in request.POST:
            return render_400("Require username parameter")
        if 'sign' not in request.POST:
            return render_400("Require sign parameter")
        user = SSUser.get_by_name(request.POST['username'])
        if user is None:
            return render_404("Cannot find user")
        if not validate_sign(request, user):
            return render_403("Forbidden")
        kwargs['user'] = user
        return func(request, *args, **kwargs)

    _wrapper.csrf_exempt = True
    return _wrapper
