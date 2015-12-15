from django.conf.urls import url
from bucketlist.views.frontend import HomePageView, RegisterView, UserDashboardView,\
                             LoginView, UpdateBucketlistView,\
                             DeleteBucketlistView, BucketlistItemView,\
                             UpdateBucketlistItemView, DeleteBucketlistItemView
from django.contrib.auth.decorators import login_required


# frontend URLs
urlpatterns = [
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
