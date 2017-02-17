import os
from django import template
from django.utils.translation import ugettext as _


register = template.Library()


@register.simple_tag
def t(message):
    if len(message) == 0:
        return message
    return _(message)


@register.simple_tag
def img_with_lang(request, path):
    lang = request.LANGUAGE_CODE.lower()
    fname, ext = os.path.splitext(path)
    return "%s.%s%s" % (fname, lang, ext)


@register.inclusion_tag('tags/paginate.html')
def paginate(models, request):
    return {'models': models, 'request': request}


@register.simple_tag
def pager_url(request, page=None):
    path = request.path
    params = request.GET.copy()
    if page:
        params['page'] = page
    return "%s?%s" % (path, params.urlencode())


@register.simple_tag
def sidebar_active(request, target):
    if hasattr(request, 'active_page'):
        current = request.active_page
        if current == target:
            return 'active'
    return ''


@register.filter
def fdate(value):
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M:%S")


@register.filter
def format_flow(value):
    value = int(value)
    if value >= 1024 * 1024 * 1024 * 1024:
        return "%.2f TB" % (value / 1024.0 / 1024.0 / 1024.0 / 1024.0)
    elif value >= 1024 * 1024 * 1024:
        return "%.2f GB" % (value / 1024.0 / 1024.0 / 1024.0)
    elif value >= 1024 * 1024:
        return "%.2f MB" % (value / 1024.0 / 1024.0)
    elif value >= 1024:
        return "%.2f KB" % (value / 1024.0)
    else:
        return "%d B" % value


@register.filter
def format_bandwidth(value):
    value = int(value)
    if value >= 1000 * 1000 * 1000 * 1000:
        return "%.2f Tbps" % (value / 1000.0 / 1000.0 / 1000.0 / 1000.0)
    elif value >= 1000 * 1000 * 1000:
        return "%.2f Gbps" % (value / 1000.0 / 1000.0 / 1000.0)
    elif value >= 1000 * 1000:
        return "%.2f Mbps" % (value / 1000.0 / 1000.0)
    elif value >= 1000:
        return "%.2f Kbps" % (value / 1000.0)
    else:
        return "%d bps" % value
