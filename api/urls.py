from django.conf.urls import include, url
from api.controllers import statistic, user

urlpatterns = [
    url(r'^statistic/post$', statistic.post_data),
    url(r'^statistic/bandwidth$', statistic.user_bandwidth),
    url(r'^statistic/connection$', statistic.user_connection),
    url(r'^statistic/server_bandwidth$', statistic.server_bandwidth),
]

urlpatterns += [
    url(r'^user/config$', user.config),
]
