from django.conf.urls import include, url
from sysadmin.controllers import login, user, server, download, license, operation_log

urlpatterns = [
    # Login
    url(r'^/?$', login.index),
    url(r'^total_bandwidth$', login.total_bandwidth),
    url(r'^login$', login.login_index),
    url(r'^do_login$', login.do_login),
    url(r'^logout$', login.do_logout),
    url(r'^change_password$', login.change_password),
]

urlpatterns += [
    # User admin
    url(r"^customers/?$", user.index),
    url(r"^customers/create$", user.create),
    url(r"^customers/(?P<id>\d+)$", user.details),
    url(r"^customers/(?P<id>\d+)/config$", user.config),
    url(r"^customers/(?P<id>\d+)/edit$", user.edit),
    url(r"^customers/(?P<id>\d+)/enable$", user.enable),
    url(r"^customers/(?P<id>\d+)/disable$", user.disable),
    url(r"^customers/(?P<id>\d+)/delete$", user.delete),
]

urlpatterns += [
    # User admin
    url(r"^servers/?$", server.index),
    url(r"^servers/create$", server.create),
    url(r"^servers/(?P<id>\d+)$", server.detail),
    url(r"^servers/(?P<id>\d+)/edit$", server.edit),
    url(r"^servers/(?P<id>\d+)/delete$", server.delete),
]

urlpatterns += [
    url(r'^download/?$', download.index),
]

urlpatterns += [
    url(r'^license/?$', license.index),
    url(r'^license/update$', license.update),
]

urlpatterns += [
    url(r'^operation_log/?$', operation_log.index),
]
