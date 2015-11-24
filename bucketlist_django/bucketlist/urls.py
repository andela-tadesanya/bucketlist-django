from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from bucketlist import views


urlpatterns = [
    url(r'^bucketlist/$', views.BucketListView.as_view(), name='bucketlists'),
    url(r'^bucketlist/(?P<id>[0-9]+)/$', views.BucketListDetailView.as_view(), name='bucketlists'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
