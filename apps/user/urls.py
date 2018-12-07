from django.conf.urls import url
from django.urls import include, path,re_path
from django.contrib.auth.decorators import login_required
# from . import views
from user.views import RegisterView,ActiveView,LoginView,UserInfoView,UserOrderView,UserSiteView,LogoutView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('', UserInfoView.as_view(), name='user'),
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),#使用正则匹配url
    re_path(r'^login', LoginView.as_view(), name='login'),#使用正则匹配url
    # re_path(r'^$', UserInfoView.as_view(), name='user'),#使用正则匹配url
    # re_path(r'^order/(?P<page>d+)/$', UserOrderView.as_view(), name='order'),#使用正则匹配url
    # re_path(r'^order/(\d+)$', UserOrderView.as_view(), name='order'),#使用正则匹配url
    re_path(r'^order/(?P<page>\d+)$', UserOrderView.as_view(), name='order'),#使用正则匹配url
    # re_path(r'^order/$', UserOrderView.as_view(), name='order'),#使用正则匹配url
    # re_path(r'^order/page<int:page>/', UserOrderView.as_view(), name='order'),#使用正则匹配url
    re_path(r'^address', UserSiteView.as_view(), name='address'),#使用正则匹配url
    re_path(r'^logout', LogoutView.as_view(), name='logout'),#使用正则匹配url
    # path('login/', LoginView.as_view(), name='login'),
    # path('register/', views.register, name='register'),
    # path('register_submit', views.register_submit, name='register_submit'),
]