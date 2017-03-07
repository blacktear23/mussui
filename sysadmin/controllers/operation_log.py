from sysadmin.views import *


@login_required
@load_license
@active_page("operation_log")
def index(request):
    begin_date, end_date = None, None
    if 'begin_date' in request.GET and request.GET['begin_date'] != "":
        pdate = parse_datetime(request.GET['begin_date'])
        if pdate is not None:
            begin_date = pdate
            end_date = pdate - timedelta(days=1)

    if 'end_date' in request.GET and request.GET['end_date'] != "" and begin_date is not None:
        pdate = parse_datetime(request.GET['end_date'])
        if pdate is not None:
            if pdate < begin_date:
                end_date = pdate

    if end_date is not None and begin_date is not None:
        query = OperationLog.objects.filter(date__gte=end_date, date__lte=begin_date)
    else:
        query = OperationLog.objects

    query = query.order_by("date").reverse()
    data = {
        'begin_date': request.GET.get('begin_date', ''),
        'end_date': request.GET.get('end_date', ''),
        'logs': paginate(request, query),
    }
    return render(request, "sysadmin/operation_log/index.html", data)
