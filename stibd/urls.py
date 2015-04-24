from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'tutor.views.home'),
    url(r'^run/', 'tutor.views.preprocess'),
    url(r'^contact/', 'tutor.views.contact'),
    url(r'^faq/', 'tutor.views.faq'),
    url(r'^register/', 'tutor.views.register'),
    url(r'^tutor/', include('tutor.urls')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^tutor_admin/', include(admin.site.urls)),
)
