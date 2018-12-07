"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include,re_path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('apps.user.urls')),
    path('order/', include('apps.order.urls')),
    path('cart/', include('apps.cart.urls')),
    path('tinymce/', include('tinymce.urls')),
    # path('search/', include('haystack.urls')),
    re_path(r'^search', include('haystack.urls')),#使用正则匹配url
    #匹配网站首页
    path('', include('apps.goods.urls')),
]