import json
import logging
from functools import wraps
from datetime import datetime
from django.shortcuts import *
from django.db.models import Q
from django.http import *
from django.template.base import add_to_builtins
from django.views.decorators.http import *
from db.models import *


def is_logined(request):
    return 'user_id' in request.session


def ulogin_required(func):
    @wraps(func)
    def _wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            return redirect("/login")
        try:
            ssuser = SSUser.objects.get(pk=request.session['user_id'])
            if ssuser:
                request.ssuser = ssuser
                return func(request, *args, **kwargs)
        except Exception as e:
            logging.info(e)
        return redirect("/login")
    return _wrapper
