from django.conf.urls import url
from django.urls import include, path
# from . import views
from order.views import OrderPlaceView, OrderCommitView

app_name = 'order'
urlpatterns = [
    path('place/', OrderPlaceView.as_view(), name='place'),
    path('commit/', OrderCommitView.as_view(), name='commit'),
]