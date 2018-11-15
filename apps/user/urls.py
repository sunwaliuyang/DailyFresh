from django.conf.urls import url
from django.urls import include, path,re_path
# from . import views
from user.views import RegisterView,ActiveView,LoginView

app_name = 'user'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    re_path(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),#使用正则匹配url
    path('login/', LoginView.as_view(), name='login'),
    # path('register/', views.register, name='register'),
    # path('register_submit', views.register_submit, name='register_submit'),
]