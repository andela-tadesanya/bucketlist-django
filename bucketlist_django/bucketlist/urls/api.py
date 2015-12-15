from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from bucketlist.views import api
from rest_framework.authtoken.views import obtain_auth_token


# bucketlist URLs
urlpatterns = [
    url(r'^bucketlist/$', api.BucketListView.as_view(), name='bucketlist_list'),
    url(r'^bucketlist/(?P<id>[0-9]+)/$', api.BucketListDetailView.as_view(), name='bucketlist_single'),
    url(r'^bucketlist/(?P<id>[0-9]+)/items/$', api.BucketListItemListView.as_view(), name='bucketlist_item_list'),
    url(r'^bucketlist/(?P<id>[0-9]+)/items/(?P<item_id>[0-9]+)/$', api.BucketListItemDetailView.as_view(), name='bucketlist_item_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)

# registration and authentication URLs
urlpatterns += [
    url(r'^token/', obtain_auth_token, name='token'),
    url(r'^users/$', api.UserCreate.as_view(), name='api_create_user'),
    url(r'^users/(?P<pk>[0-9]+)/$', api.UserDetail.as_view(), name='api_get_user'),
]

# django swagger URLs
urlpatterns += [
    url(r'^docs/', include('rest_framework_swagger.urls')),
]
