from django.conf.urls import url
from django.urls import include, path
from . import views

app_name = 'user'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('register_submit', views.register_submit, name='register_submit'),
]