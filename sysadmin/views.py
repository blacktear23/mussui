import json
from datetime import datetime
from django.shortcuts import *
from django.db.models import Q
from django.http import *
from django.template.base import add_to_builtins
from django.forms.models import model_to_dict, save_instance
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import *
from db.models import *
from sysadmin.forms import *


add_to_builtins("django.templatetags.i18n")
add_to_builtins("sysadmin.templatetags.tags")


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
