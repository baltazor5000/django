from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
import contacts.views

urlpatterns = patterns('',
    url(r'^$', contacts.views.ListContactView.as_view(),
        name='contacts-list'),

    url(r'^new$', contacts.views.CreateContactView.as_view(),
        name='contacts-new'),

    url(r'^edit/(?P<pk>\d+)/$', contacts.views.UpdateContactView.as_view(),
        name='contacts-edit'),

    url(r'^delete/(?P<pk>\d+)/$', contacts.views.DeleteContactView.as_view(),
        name='contacts-delete'),

    url(r'^(?P<pk>\d+)/$', contacts.views.ContactView.as_view(),
        name='contacts-view',),

    url(r'^edit/(?P<pk>\d+)/addresses$', contacts.views.EditContactAddressView.as_view(),
        name='contacts-edit-addresses',),

    url(r'^search/$', contacts.views.SearchContactView.as_view(),
        name='contacts-search'),

    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
)

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)