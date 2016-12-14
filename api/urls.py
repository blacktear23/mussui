from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.controllers.statistic',
    url(r'^statistic/post$', 'post_data'),
    url(r'^statistic/bandwidth$', 'user_bandwidth'),
    url(r'^statistic/connection$', 'user_connection'),
)

urlpatterns += patterns('api.controllers.user',
    url(r'^user/config$', 'config'),
)
