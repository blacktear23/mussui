from django import template
from django.utils.translation import ugettext as _


register = template.Library()


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
    return value.strftime("%Y-%m-%d %H:%M:%S")
