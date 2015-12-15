"""bucketlist_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from bucketlist.views import HomePageView, RegisterView, UserDashboardView,\
                             LoginView, UpdateBucketlistView,\
                             DeleteBucketlistView, BucketlistItemView,\
                             UpdateBucketlistItemView, DeleteBucketlistItemView
from django.contrib.auth.decorators import login_required


urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include('bucketlist.urls', namespace='bucketlist')),
]

# frontend URLs
urlpatterns += [
    url(r'^$', HomePageView.as_view(), name='homepage'),
    url(r'^register/$', RegisterView.as_view(), name='register_user'),
    url(r'^authentication/$', LoginView.as_view(), name='authentication'),
    url(r'^user/$', login_required(UserDashboardView.as_view()), name='dashboard'),
    url(r'^bucketlist/update/$', login_required(UpdateBucketlistView.as_view()), name='update_bucketlist'),
    url(r'^bucketlist/delete/$', login_required(DeleteBucketlistView.as_view()), name='delete_bucketlist'),
    url(r'^user/bucketlist/(?P<id>[0-9]+)/items/$', login_required(BucketlistItemView.as_view()), name='bucketlist_items'),
    url(r'^user/bucketlist/(?P<id>[0-9]+)/items/update/$', login_required(UpdateBucketlistItemView.as_view()), name='update_bucketlist_items'),
    url(r'^user/bucketlist/(?P<id>[0-9]+)/items/delete/$', login_required(DeleteBucketlistItemView.as_view()), name='delete_bucketlist_items'),
]
