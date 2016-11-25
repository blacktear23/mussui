from django.conf.urls import patterns, include, url

urlpatterns = patterns('sysadmin.controllers.login',
    # Login
    url(r'^/?$', 'index'),
    url(r'^login$', 'login_index'),
    url(r'^do_login$', 'do_login'),
    url(r'^logout$', 'do_logout'),
    url(r'^change_password$', 'change_password'),
)

urlpatterns += patterns('sysadmin.controllers.user',
    # User admin
    url(r"^customers/?$", 'index'),
    url(r"^customers/create$", 'create'),
    url(r"^customers/(?P<id>\d+)$", 'details'),
    url(r"^customers/(?P<id>\d+)/config$", 'config'),
    url(r"^customers/(?P<id>\d+)/edit$", 'edit'),
    url(r"^customers/(?P<id>\d+)/enable$", 'enable'),
    url(r"^customers/(?P<id>\d+)/disable$", 'disable'),
    url(r"^customers/(?P<id>\d+)/delete$", 'delete'),
)

urlpatterns += patterns('sysadmin.controllers.server',
    # User admin
    url(r"^servers/?$", 'index'),
    url(r"^servers/create$", 'create'),
    url(r"^servers/(?P<id>\d+)$", 'detail'),
    url(r"^servers/(?P<id>\d+)/edit$", 'edit'),
    url(r"^servers/(?P<id>\d+)/delete$", 'delete'),
)

urlpatterns += patterns('sysadmin.controllers.download',
    url(r'^download/?$', 'index'),
)
