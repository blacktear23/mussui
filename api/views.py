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
