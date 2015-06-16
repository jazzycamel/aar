from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from aar.views import *

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^home/$', home, name="home"),
    url(r'^venue/$', venue, name="venue"),
    url(r'^travel/$', travel, name="travel"),
    url(r'^accommodation/$', accommodation, name="accommodation"),
    url(r'^contact/$', contact, name="contact"),
    url(r'^create/person/$', createPerson, name="createPerson"),
    url(r'^create/address/$', createAddress, name="createAddress"),
    url(r'^create/invitation/$', createInvitation, name="createInvitation"),
    url(r'^create/saveTheDates/$', createSaveTheDates, name="createSaveTheDates"),
    url(r'^create/meal/$', createMeal, name="createMeal"),
    url(r'^create/tables/$', createTables, name='createTables'),
    url(r'^create/invitations/$', createInvitations, name="createInvitations"),
    url(r'^view/peopleForAddress/$', getPeopleForAddress, name="getPeopleForAddress"),
    url(r'^rsvp/$', rsvp, name='rsvp'),
    url(r'^rsvp/(?P<invitationNum>[0-9]+)/$', rsvp, name='rsvp'),
    url(r'^meal/$', meal, name='meal'),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)