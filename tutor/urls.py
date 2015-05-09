from django.conf.urls import patterns, include, url
#aca
from django.views.generic import DetailView, ListView
from tutor.models import *
'''
urlpatterns = patterns('',
    url(r'^$',
        ListView.as_view(
            queryset=Poll.objects.order_by('-pub_date')[:5],
            context_object_name='latest_poll_list',
            template_name='tutor/index.html')),
    url(r'^(?P<pk>\d+)/$',
        DetailView.as_view(
            model=Poll,
            template_name='tutor/detail.html')),
    url(r'^(?P<pk>\d+)/results/$',
        DetailView.as_view(
            model=Poll,
            template_name='tutor/results.html'),
        name='poll_results'),
    url(r'^(?P<poll_id>\d+)/vote/$', 'tutor.views.vote'),
    url(r'^$', 'tutor.views.home'),
    url(r'^login/$', 'tutor.views.login_call'),
    url(r'^logout/$', 'tutor.views.logout_call'),
)#taca
'''
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('tutor.views',
    url(r'^$', 'index'),
    url(r'^login/$', 'login_call'),
    url(r'^logout/$', 'logout_call'),
    url(r'^registration/$', 'register_call'),
    url(r'^run/$', 'preprocess'),
    url(r'^contact/', 'contact'),
    url(r'^faq/', 'faq'),
    url(r'^register/', 'register'),
    url(r'^question/$', 'question_ajax'),
    url(r'^alternative/$', 'alternative_ajax'),
)
urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    #url(r'^tutor_admin/', include(admin.site.urls)),
)
