from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^special/all/', views.AllView.as_view(), name='page_list'),
    url(r'^special/tags/', views.TagView.as_view(), name='tag_list'),
    url(r'^special/recent/', views.RecentView.as_view(), name='recent_list'),
    url(r'^search', views.search, name='search'),
    url(r'^special/create', views.create, name='create'),
    url(r'^(?P<title>[^/]+)$', views.view, name='djiki-page-view'),
    url(r'^(?P<title>[^/]+)/edit/$', views.edit, name='djiki-page-edit'),
    url(r'^(?P<title>[^/]+)/history/$', views.history, name='djiki-page-history'),
    url(r'^(?P<title>[^/]+)/history/(?P<revision_pk>[0-9]+)/$', views.view, name='djiki-page-revision'),
    url(r'^(?P<title>[^/]+)/diff/$', views.diff, name='djiki-page-diff'),
    url(r'^(?P<title>[^/]+)/undo/(?P<revision_pk>[0-9]+)/$', views.undo, name='djiki-page-undo'),
    url(r'^(?P<title>[^/]+)/revert/(?P<revision_pk>[0-9]+)/$', views.revert, name='djiki-page-revert'),
    url(r'^image/$', views.image_new, name='djiki-image-new'),
    url(r'^image/(?P<name>[^/]+)$', views.image_view, name='djiki-image-view'),
    url(r'^image/(?P<name>[^/]+)/edit/$', views.image_edit, name='djiki-image-edit'),
    url(r'^image/(?P<name>[^/]+)/history/$', views.image_history, name='djiki-image-history'),
    url(r'^$','django.views.generic.simple.redirect_to', {'url': u'/wiki/Main_Page'}),
    )
