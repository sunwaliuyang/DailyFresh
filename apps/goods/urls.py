
from django.conf.urls import url
from django.urls import include, path
from goods.views import IndexView,ListView,DetailView

app_name = 'goods'
urlpatterns = [
    # path('', views.index, name='index'),
    path('', IndexView.as_view(), name='index'),
    path('goods/<int:goods_id>', DetailView.as_view(), name='detail'),
    path('list/<int:type_id>/<int:page>', ListView.as_view(), name='list'),
]