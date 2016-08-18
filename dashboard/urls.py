from django.conf.urls import url

from dashboard import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^accounts$', views.accounts, name='accounts'),
    url(r'^acme$', views.acme, name='acme'),
    url(r'^burlington$', views.burlington, name='burlington'),
    url(r'^leads_and_quotes$', views.leads_and_quotes, name='leads_and_quotes'),
    url(r'^export_transaction_data$', views.export_transaction_data, name='export_transaction_data'),
]
