from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout_then_login


app_name = 'portal'

urlpatterns = [
    url(r'^$', views.home, name='home'),
    # url(r'^portal_login/$', views.portal_login, name='portal_login'),
    url(r'^campaigns/$', views.campaigns, name='campaigns'),
    url(r'^get_prospect/(?P<campaign_id>[0-9]+)/$', views.get_prospect, name='get_prospect'),
    # url(r'^updated_prospect/(?P<prospect_id>[0-9]+)')
    url(r'^campaign/(?P<campaign_id>[0-9]+)/$', views.campaign_details, name='campaign_details'),
    url(r'^make_lead/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$', views.make_lead, name='make_lead'),
    url(r'^make_dnc/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$', views.make_dnc, name='make_dnc'),
    url(r'^make_view/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$', views.make_view, name='make_view'),
    url(r'^make_changes/(?P<campaign_id>[0-9]+)/(?P<prospect_id>[0-9]+)/$', views.make_changes, name='make_changes'),
    url(r'^my_leads/(?P<campaign_id>[0-9]+)/$', views.my_leads, name='my_leads'),
    url(r'^my_views/(?P<campaign_id>[0-9]+)/$', views.my_views, name='my_views'),
    url(r'^my_dncs/(?P<campaign_id>[0-9]+)/$', views.my_dncs, name='my_dncs'),
    url(r'^login/$', login, {'template_name': 'portal/portal_login.html'}, name='login'),
    url(r'^logout/$', logout_then_login, name='logout'),

]