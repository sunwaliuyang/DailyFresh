
from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = 'goods'
urlpatterns = [
    path('', views.index, name='index'),
]