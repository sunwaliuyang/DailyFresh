from django.conf.urls import url
from django.urls import include, path,re_path
# from . import views
from order.views import OrderPlaceView, OrderCommitView, OrderPayView, CheckPayView,CommentView


app_name = 'order'
urlpatterns = [
    path('place/', OrderPlaceView.as_view(), name='place'),
    path('commit', OrderCommitView.as_view(), name='commit'),
    path('pay', OrderPayView.as_view(), name='pay'),
    path('check', CheckPayView.as_view(), name='check'),
    re_path('comment/(?P<order_id>.*)$', CommentView.as_view(), name='comment'),
    # path('comment/<int:order_id>', CommentView.as_view(), name='comment'),
]