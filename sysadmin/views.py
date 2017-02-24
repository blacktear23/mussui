import json
from functools import wraps
from datetime import datetime, timedelta
from django.shortcuts import *
from django.db.models import Q
from django.http import *
from django.template.base import add_to_builtins
from django.forms.models import model_to_dict, save_instance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import *
from db.models import *
from monitor.models import *
from sysadmin.forms import *


add_to_builtins("django.templatetags.i18n")
add_to_builtins("sysadmin.templatetags.tags")


def active_page(page):
    def active_page_wrapper(func):
        @wraps(func)
        def _wrapper(request, *args, **kwargs):
            request.active_page = page
            return func(request, *args, **kwargs)
        return _wrapper
    return active_page_wrapper


def load_license(func):
    @wraps(func)
    def _wrapper(request, *args, **kwargs):
        request.license = License.get_or_init()
        if request.license is not None:
            request.license_config = request.license.get_config()
        return func(request, *args, **kwargs)
    return _wrapper


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


def render_form_error(form):
    ret = {}
    for key, value in form.errors.items():
        ret[key] = value[0]
    return render_json(ret, 400)


def parse_datetime(value):
    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M",
        "%Y-%m-%d",
    ]
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt)
        except:
            pass
    return None


def paginate(request, query, per_page=30):
    # if we got a empty query then just return it
    try:
        count = query.count()
    except (AttributeError, TypeError):
        count = len(query)
    if count == 0:
        return query
    page = request.GET.get('page')
    # Get per_page in request
    if 'per_page' in request.GET:
        try:
            per_page = int(request.GET['per_page'])
        except Exception:
            pass
    # generate page
    paginator = Paginator(query, per_page)
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        return paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return paginator.page(paginator.num_pages)


def log_request(request, target, message):
    operator = request.user.username
    OperationLog.log(operator, target, message)
