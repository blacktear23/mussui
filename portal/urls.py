from django.conf.urls import include, url
from portal.controllers import index, login

urlpatterns = [
    # Index
    url(r'^/?$', index.index),
    # Login
    url(r'^login$', login.login_index),
    url(r'^do_login$', login.do_login),
    url(r'^logout$', login.do_logout),
    url(r'^change_password$', login.change_password),
]
