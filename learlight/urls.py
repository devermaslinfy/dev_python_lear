from django.conf.urls import include, url
from django.contrib import admin

from learlight import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^signed_s3_request/$', views.signed_s3_request, name='signed_s3_request'),
    url(r'^dashboard', include('dashboard.urls', namespace='dashboard')),
    url(r'^customer/', include('crm.urls', namespace='crm')),
    url(r'^admin/', include(admin.site.urls)),
]
