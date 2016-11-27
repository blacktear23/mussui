from django.conf.urls import include, url

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^admin/', include('sysadmin.urls')),
    url(r'^', include('portal.urls')),
]
