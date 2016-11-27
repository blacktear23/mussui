from django.conf.urls import patterns, include, url

urlpatterns = patterns('portal.controllers',
    # Index
    url(r'^/?$', 'index.index'),
    # Login
    url(r'^login$', 'login.login_index'),
    url(r'^do_login$', 'login.do_login'),
    url(r'^logout$', 'login.do_logout'),
)
