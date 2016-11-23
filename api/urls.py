from django.conf.urls import patterns, include, url

urlpatterns = patterns('api.controllers.statistic',
    url(r'^statistic/post$', 'post_data'),
    url(r'^statistic/bandwidth$', 'user_bandwidth'),
)
