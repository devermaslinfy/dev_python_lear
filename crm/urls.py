from django.conf.urls import url

from crm import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<associate_id>[\d]+)/how_to_proceed$', views.how_to_proceed, name='how_to_proceed'),
    url(r'^authorization/(?P<customer_id>[\d]+)$', views.authorization, name='authorization'),
    url(r'^information/(?P<customer_id>[\d]+)$', views.information, name='information'),
    url(r'^email_photo/(?P<customer_id>[\d]+)$', views.email_photo, name='email_photo'),
    url(r'^quote_create/(?P<customer_id>[\d]+)$', views.quote_create, name='quote_create'),
    url(r'^quote_summary/(?P<customer_id>[\d]+)$', views.quote_summary, name='quote_summary'),
    url(r'^quote_confirmation/(?P<customer_id>[\d]+)$', views.quote_confirmation, name='quote_confirmation'),
    url(r'^email_photo_confirmation/(?P<customer_id>[\d]+)$', views.email_photo_confirmation, name='email_photo_confirmation'),
]
